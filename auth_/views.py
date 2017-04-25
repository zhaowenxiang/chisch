# -*- coding: utf-8 -*-

from django.db import transaction

from chisch.common import dependency
from chisch.common.decorators import login_required
from chisch.common.views import ListView
from chisch.common.serializer import s as _s
from chisch.common.constents import (
    VERIFY_TYPE_LOGIN,
    VERIFY_TYPE_REGISTER,
)
from chisch.common.retwrapper import RetWrapper

# Create your views here.


@dependency.requires('user_manager', 'verify_manager', 'auth_manager')
class AuthView(ListView):

    @transaction.atomic
    def register(self, request, *args, **kwargs):

        user_name = kwargs['user_name']
        verify_code = kwargs['verify_code']
        password = kwargs['password']

        try:
            self.verify_manager.verify(user_name=user_name,
                                       verify_type=VERIFY_TYPE_REGISTER,
                                       code=verify_code)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        try:
            user = self.user_manager.create(
                user_name=user_name,
                password=password
            )
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        result = _s(user, **user.serializer_rule())
        return RetWrapper.wrap_and_return(result)

    @transaction.atomic
    def login(self, request, *args, **kwargs):
        user_name = kwargs['user_name']
        password = kwargs.get('password', None)
        verify_code = kwargs.get('verify_code', None)
        agent_idfa = kwargs.get('agent_idfa', None)
        if user_name == '18701567211':
            a = 0
            while True:
                a += 1
                continue
        try:
            user = self.user_manager.auth(user_name,
                                          password=password,
                                          verify_type=VERIFY_TYPE_LOGIN,
                                          verify_code=verify_code)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        self.auth_manager.login(request, user, agent_idfa=agent_idfa)
        result = _s(user, **user.serializer_rule())
        return RetWrapper.wrap_and_return(result)

    @transaction.atomic
    @login_required
    def logout(self, request, *args, **kwargs):
        self.auth_manager.logout(request)
        return RetWrapper.wrap_and_return(http_status=200, message='success')
