# -*- coding: utf-8 -*-

import logging

from django.db import transaction

from chisch.common import dependency
from chisch.common.decorators import login_required
from chisch.common.retwrapper import RetWrapper
from chisch.common.serializer import s as _s
from chisch.common.views import ListView


logger = logging.getLogger('django')


@dependency.requires('work_order_manager')
class WorkOrderListView(ListView):

    @login_required
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        order_type = kwargs['type']
        try:
            work_order = self.work_order_manager.create(user_id, order_type)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)

        result = _s(work_order)
        return RetWrapper.wrap_and_return(result)

    def verify(self, request, *args, **kwargs):
        user_name = kwargs['user_name']
        verify_type = kwargs['verify_type']
        verify_code = kwargs['verify_code']

        try:
            self.verify_manager.verify(user_name=user_name,
                                       verify_type=verify_type,
                                       code=verify_code)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        else:
            return RetWrapper.wrap_and_return(http_status=200,
                                              message='success')

