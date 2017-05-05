# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import CurriculumListView

urlpatterns = [
    url(r'^$', CurriculumListView.as_view()),
]
