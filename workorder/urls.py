# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import WorkOrderListView

urlpatterns = [
    url(r'^$', WorkOrderListView.as_view(), name='work_order'),
]
