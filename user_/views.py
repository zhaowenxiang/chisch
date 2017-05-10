# -*- coding: utf-8 -*-

import logging

import oss2
from django.conf import settings
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
class UserListView(ListView):

    @transaction.atomic
    def change_password(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_name = kwargs['user_name']
        new_password = kwargs['new_password']
        old_password = kwargs.get('old_password', None)
        verify_code = kwargs.get('verify_code', None)
        agent_idfa = kwargs['agent_idfa']

        try:
            user = self.user_manager.auth(user_name,
                                          password=old_password,
                                          verify_type=VTCP,
                                          verify_code=verify_code)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)

        user.set_password(new_password)
        user.save()
        token = self.auth_manager.login(request,
                                        user,
                                        agent_idfa=agent_idfa,
                                        flush_all_token=True)
        result = _s(user, extra={'access_token': token})
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
        mobile_number = kwargs['mobile_number']
        verify_code = kwargs['verify_code']
        agent_idfa = kwargs['agent_idfa']
        password = kwargs['password']
        try:
            self.verify_manager.verify(user_name=mobile_number,
                                       verify_type=VTCMN,
                                       code=verify_code)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        try:
            user = self.user_manager.auth(request.user.mobile_number,
                                          password=password,
                                          verify_type=VTCP)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)

        if user.display_name == user.mobile_number:
            user.display_name = mobile_number
        user.mobile_number = mobile_number

        user.save()
        access_token = self.auth_manager.login(request,
                                               user,
                                               agent_idfa=agent_idfa,
                                               flush_all_token=True)
        result = _s(user, extra={'access_token': access_token})
        return RetWrapper.wrap_and_return(result)

    @login_required
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            user = self.user_manager.update(request.user, **kwargs)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        result = _s(user)
        return RetWrapper.wrap_and_return(result)

    @login_required
    @transaction.atomic
    def upload_avatar(self, request, *args, **kwargs):
        from oss.cores import get_object_key
        user = request.user
        f = kwargs['files'][0]
        key = get_object_key('upload_user_avatar', user.id, settings.IMAGE_TYPE)
        permission = oss2.OBJECT_ACL_PUBLIC_READ
        try:
            avatar_url, _ = self.oss_manager.single_object_upload(key, f,
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
        result = _s(user)
        return RetWrapper.wrap_and_return(result)


@dependency.requires('user_manager', 'verification_manager')
class UserDetailView(DetailView):

    def get(self, request, *args, **kwargs):
        user_id = args[0]
        user = self.user_manager.get(id=user_id)
        token_user_id = request.user.id if request.user.is_authenticated \
            else None
        result = _s(user, **user.serializer_rule(user.id, token_user_id))
        return RetWrapper.wrap_and_return(result)


