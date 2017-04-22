# -*- coding: utf-8 -*-

import logging

from django.db import transaction

from chisch.common import dependency
from chisch.common.retwrapper import RetWrapper
from chisch.common.serializer import s as _s
from chisch.common.views import DetailView

from chisch.utils.clientutils import ClientInfoGenerator


logger = logging.getLogger('django')


@dependency.requires('user_manager', 'verify_manager')
class VerifyListView(DetailView):

    @transaction.atomic
    def gain(self, request, *args, **kwargs):
        user_name = kwargs['user_name']
        verify_type = kwargs['verify_type']
        ip = ClientInfoGenerator.get_client_ip(request)

        try:
            verify_code = self.verify_manager.create(user_name=user_name,
                                                     verify_type=verify_type,
                                                     ip=ip)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)

        result = _s(verify_code)
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

