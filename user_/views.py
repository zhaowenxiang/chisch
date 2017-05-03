# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.db import transaction

from chisch.common import upload_file_analysis as ufa

from chisch.common.retwrapper import RetWrapper
from chisch.common import dependency
from chisch.common.decorators import login_required
from chisch.common.views import ListView, DetailView
from chisch.common.serializer import s as _s
from chisch.common.constents import (
    VERIFY_TYPE_CHANGE_PASSWORD as VTCP,
)


logger = logging.getLogger('django')


@dependency.requires('user_manager',
                     'verify_manager',
                     'auth_manager',
                     'oss_manager')
class UserDetailView(DetailView):

    @login_required
    def get(self, request, *args, **kwargs):
        # TODO
        user = self.user_manager.get(id=request.user.id)
        result = _s(user, **user.serializer_rule())
        return RetWrapper.wrap_and_return(result)

    @transaction.atomic
    def change_password(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_name = args[0]
        new_password = kwargs.get('new_password', None)
        old_password = kwargs.get('old_password', None)
        verify_code = kwargs.get('verify_code', None)
        agent_idfa = kwargs.get('agent_idfa', None)

        try:
            user = self.user_manager.auth(user_name,
                                          password=old_password,
                                          verify_type=VTCP,
                                          verify_code=verify_code)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)

        user.set_password(new_password)
        user.save()
        self.auth_manager.login(request,
                                user,
                                agent_idfa=agent_idfa,
                                flush_all_token=True)
        result = _s(user, **user.serializer_rule())
        return RetWrapper.wrap_and_return(result)

    @login_required
    @transaction.atomic
    def update(self, request, *args, **kwargs):

        user = self.user_manager.update(request.user, **kwargs)
        result = _s(user, **user.serializer_rule())
        return RetWrapper.wrap_and_return(result)

    @login_required
    @transaction.atomic
    def upload_user_avatar(self, request, *args, **kwargs):
        user = request.user
        arguments, files = ufa.parse_multipart_form_data(body=request.body)
        from oss.cores import get_object_key
        key = get_object_key(request.GET.get('action'),
                             user.id,
                             files[0]['file_type'])
        try:
            resp = self.oss_manager.single_object_direct_upload(key, files[0])
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        if str(resp.status).startswith('20'):
            aliyun_oss = settings.ALIYUN_OSS
            backup_name = aliyun_oss['BUCKET_NAME']
            endpoint = aliyun_oss['ENDPOINT']
            user.avatar_url = endpoint.replace('://',
                                               '://' + backup_name + '.') + key
            user.save()
        else:
            return RetWrapper.wrap_and_return(message='server error',
                                              http_status=500)
        result = _s(user, **user.serializer_rule())
        return RetWrapper.wrap_and_return(result)


@dependency.requires('user_manager', 'verification_manager')
class UserListView(ListView):
    pass


