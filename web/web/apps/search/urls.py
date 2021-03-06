# -*- coding: utf-8 -*-

__copyright__ = """ Copyright (c) 2018 Newton Foundation. All rights reserved."""
__version__ = '1.0'
__author__ = 'tony.liu@diynova.com'

from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
                       url(r'^$', views.IdListView.as_view()),
                       )
