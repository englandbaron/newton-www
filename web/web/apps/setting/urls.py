from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^gtoken/$', views.show_set_gtoken_view),
                       url(r'^gtoken/check/$', views.show_check_gtoken_view),
                       url(r'^gtoken/post/$', views.submit_gtoken),
)
