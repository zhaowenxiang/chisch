# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import (
    UserListView,
    UserDetailView,
)

urlpatterns = [
    url(r'^$', UserListView.as_view()),
    url(r'^/([1-9]\d*|0)$', UserDetailView.as_view()),
]

