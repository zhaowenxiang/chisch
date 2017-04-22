# -*- coding: utf-8 -*-

import logging
import simplejson

import oss2
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
from django.conf import settings
from django.db import transaction


from chisch.common import dependency
from chisch.common.retwrapper import RetWrapper
from chisch.common.serializer import s as _s
from chisch.common.views import DetailView


@dependency.requires('user_manager', 'oss_manager')
class OssDetail(DetailView):

    def get_sts_token(self, request):

        sts_token = self.oss_manager.create_sts_token(request)

        result = _s(sts_token)
        return RetWrapper.wrap_and_return(result)

