# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from chisch.common.retwrapper import RetWrapper
from chisch.common import dependency


@dependency.requires('auth_manager')
class AuthenticationMiddleware(object):

    def _recognise_access_token(self, request):
        """
        识别token，解析出user
        :param request:
        :return:(access_token, user)
        """
        token_name = 'HTTP_' + settings.ACCESS_TOKEN_NAME.upper() \
                                                         .replace('-', '_')
        access_token = request.META.get(token_name, None)
        if not access_token:
            return None, AnonymousUser()
        user = self.auth_manager.recognise_access_token(
                                                    access_token=access_token)
        return access_token, user

    def process_request(self, request):
        try:
            access_token, user = self._recognise_access_token(request)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        request.access_token = access_token
        request.user = user
