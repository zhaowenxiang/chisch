# -*- coding: utf-8 -*-

import logging

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
from chisch.utils.stringutils import hide_mobile_number


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
        access_token = self.auth_manager.login(request,
                                               user,
                                               agent_idfa=agent_idfa,
                                               flush_all_token=True)
        result = _s(user, extra={'access_token': access_token})
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

        if user.display_name == hide_mobile_number(user.mobile_number):
            user.display_name = hide_mobile_number(mobile_number)
        user.mobile_number = mobile_number

        try:
            user.save()
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
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
        user = request.user
        image_file = kwargs['files'][0]
        try:
            avatar_url = self.user_manager.upload_avatar(user.id, image_file)
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
        user_id = int(args[0])
        try:
            user = self.user_manager.detail(user_id=user_id)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        token_user_id = request.user.id if request.user.is_authenticated \
            else None
        if user_id == token_user_id:
            extra = {'account': user.account}
            result = _s(user, extra=extra)
        else:
            result = _s(user, own=False)
        return RetWrapper.wrap_and_return(result)


