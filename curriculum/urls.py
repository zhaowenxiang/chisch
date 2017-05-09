# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import CurriculumListView, CurriculumCategoryListView

urlpatterns = [
    url(r'^$', CurriculumListView.as_view()),
    url(r'^/category$', CurriculumCategoryListView.as_view()),
]
