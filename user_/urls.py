# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import (
    UserListView,
    UserDetailView,
)

urlpatterns = [
    url(r'^$', UserListView.as_view()),
    url(r'^/([^0][0-9]*)$', UserDetailView.as_view()),
]
