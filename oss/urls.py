# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import OssDetail

urlpatterns = [
    url(r'^', OssDetail.as_view()),
]
