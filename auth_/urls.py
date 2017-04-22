# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import AuthView

urlpatterns = [
    url(r'^$', AuthView.as_view()),
]
