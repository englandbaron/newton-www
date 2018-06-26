#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

class GtokenForm(forms.Form):
    gtoken_code = forms.CharField(max_length=100, label=_("Google Authenticator Code"), required=True)
    
class SubmitGtokenForm(forms.Form):
    gtoken_code = forms.CharField(max_length=100, required=True)
    redirect_url = forms.CharField(max_length=100, required=True)