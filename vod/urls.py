# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import signature_url

urlpatterns = [
    url(r'^$', signature_url, name='signature_url'),
]
