from django.shortcuts import render

import json
import re
import logging
import requests

from django.http import HttpResponse
from django.template import Template, Context, loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.forms.forms import NON_FIELD_ERRORS
from ratelimit.decorators import ratelimit

from subscription import models as subscription_model
from config import codes
from utils import http, security
from tasks import task_email
from . import forms
from ishuman import services as ishuman_services


logger = logging.getLogger(__name__)

#@ratelimit(key='ip', rate='1/m', method=['GET','POST'])
@require_http_methods(["POST"])
def subscribe(request):
    """
    Add email address to email list database.
    User can add email once per minute.
    """
    try:
        # check robot
        form = forms.SubscribeForm(request.POST)
        if not form.is_valid():
            return http.JsonErrorResponse(error_message=_("Email Error"))
        code = form.cleaned_data['code']
        if code != ishuman_services.get_captcha(request.session.session_key):
            return http.JsonErrorResponse(error_message=_("Authenticator Recaptcha Error"))
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return http.JsonErrorResponse(error_message=_("You can only subscribe once per minute."))
        email_address = form.cleaned_data['email_address']
        subscribed_email = subscription_model.SubscribedEmail.objects.filter(email_address=email_address).first()
        if subscribed_email:
            if subscribed_email.status == codes.StatusCode.RELEASE.value:
                return http.JsonErrorResponse(error_message=_('Email Has Exist!'))
            else:
                is_send_success = do_send_mail(subscribed_email, request)
                if is_send_success:
                    return http.JsonSuccessResponse(data={"msg": _("we've sent you a confirming e-mail,please check your email box.")})
                else:
                    return http.JsonErrorResponse(error_message=_("Subscribe Failed!"))
        else:
            subscribed_email = subscription_model.SubscribedEmail(email_address=email_address)
            subscribed_email.uuid = security.generate_uuid()
            subscribed_email.save()
            is_send_success = do_send_mail(subscribed_email, request)
            if is_send_success:
                return http.JsonSuccessResponse(data={"msg": _("we've sent you a confirming e-mail,please check your email box.")})
            else:
                return http.JsonErrorResponse(error_message=_("Subscribe Failed!"))
    except ValidationError:
        return http.JsonErrorResponse(error_message=_("Invalid Email Address!"))
    except Exception, inst:
        logger.error("fail to subscribe: %s" % str(inst))
        return http.JsonErrorResponse()


def subscribed_confirm(request):
    try:
        uuid = request.GET['uuid']
        subscribed_email = subscription_model.SubscribedEmail.objects.filter(uuid=uuid).first()
        if subscribed_email:
            code = subscribed_email.status
            if code == codes.StatusCode.AVAILABLE.value:
                subscribed_email.status = codes.StatusCode.RELEASE.value
                subscribed_email.save()
            return render(request, 'subscription/confirm.html')
        else:
            logger.error("fail to find email by uuid: %s" % str(uuid))
            error_message = _("Links expire or invalid pages.")
            return render(request, "subscription/subscribe_failed.html", locals())
    except Exception, inst:
        logger.error("fail to confirm email: %s" % str(inst))
        return http.JsonErrorResponse()

def do_send_mail(subscribed_email, request):
    subject = _("NewtonProject Notifications: Please Confirm Subscription")
    targetUrl = settings.BASE_URL + "/subscribe/confirmed/?uuid=" + str(subscribed_email.uuid)
    try:
        template = loader.get_template("subscription/subscription-letter.html")
        context = Context({"targetUrl":targetUrl,"request":request})
        html_content = template.render(context)
        to_email = subscribed_email.email_address
        from_email = settings.FROM_EMAIL
        task_email.send_email.delay(subject, html_content, from_email, [to_email])
        return True
    except Exception,inst:
        logger.error("fail to send email: %s" % str(inst))
        return False
