# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import VerifyListView

urlpatterns = [
    url(r'^$', VerifyListView.as_view(), name='get_validate_code'),
]
