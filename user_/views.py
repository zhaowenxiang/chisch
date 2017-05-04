# -*- coding: utf-8 -*-

import logging
import sys

import oss2
from django.db import transaction

from chisch.common.retwrapper import RetWrapper
from chisch.common import dependency
from chisch.common.decorators import login_required
from chisch.common.views import ListView, DetailView
from chisch.common.serializer import s as _s
from chisch.common.constents import (
    VERIFY_TYPE_CHANGE_PASSWORD as VTCP,
    VERIFY_TYPE_CHANGE_MOBILE_NUMBER as VTCMN,
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
    def change_mobile_number(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_name = args[0]
        mobile_number = kwargs['mobile_number']
        verify_code = kwargs['verify_code']
        agent_idfa = kwargs['agent_idfa']
        password = kwargs['password']
        try:
            self.verify_manager.verify(user_name=user_name,
                                       verify_type=VTCMN,
                                       code=verify_code)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        try:
            user = self.user_manager.auth(user_name,
                                          password=password,
                                          verify_type=VTCP)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)

        user.mobile_number = mobile_number
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
        from oss.cores import get_object_key
        user = request.user
        action = sys._getframe().f_code.co_name
        f = kwargs['files'][0]
        key = get_object_key(action, user.id, f['type'])
        permission = oss2.OBJECT_ACL_PUBLIC_READ
        try:
            avatar_url = self.oss_manager.single_object_upload(key, f,
                                                               permission)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        if user.avatar_url:
            pass
        else:
            user.avatar_url = avatar_url
            try:
                user.save()
            except Exception, e:
                return RetWrapper.wrap_and_return(e)
        result = _s(user, **user.serializer_rule())
        return RetWrapper.wrap_and_return(result)


@dependency.requires('user_manager', 'verification_manager')
class UserListView(ListView):
    pass


