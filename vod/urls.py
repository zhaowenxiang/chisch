# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import video_upload_init

urlpatterns = [
    url(r'^$', video_upload_init, name='video_upload_init'),
]
