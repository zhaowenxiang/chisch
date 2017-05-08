# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import VideoListView

urlpatterns = [
    url(r'^$', VideoListView.as_view()),
]
