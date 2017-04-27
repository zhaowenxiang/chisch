# -*- coding: utf-8 -*-

import cgi
import logging
import struct

from gp.fileupload import Storage
from gp.fileupload import purge_files

from django.db import transaction

from chisch.common.retwrapper import RetWrapper
from chisch.common import dependency
from chisch.common.decorators import login_required
from chisch.common.views import ListView, DetailView
from chisch.common.serializer import s as _s
from chisch.common.constents import (
    VERIFY_TYPE_CHANGE_PASSWORD as VTCP,
)


logger = logging.getLogger('django')


@dependency.requires('user_manager', 'verify_manager', 'auth_manager')
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

    @transaction.atomic
    def upload_avatar(self, request, *args, **kwargs):
        a, = struct.unpack('i', request.body)
        b = 10
        #
        # fields = cgi.FieldStorage(fp=request.environ['wsgi.input'],
        #                           environ=request.environ,
        #                           keep_blank_values=1)
        # image_str = kwargs['image']
        # import base64
        # with open('/root/a.png', 'wb') as fout:
        #     fout.write(base64.b64decode(image_str))
        # try:
        #     user = self.user_manager.upload_avatar()
        # except Exception, e:
        #     return RetWrapper.wrap_and_return(e)
        # return RetWrapper.wrap_and_return(user)


@dependency.requires('user_manager', 'verification_manager')
class UserListView(ListView):
    pass


def _to_unicode(s, encoding='utf-8'):
    return s.decode('utf-8')


class MultipartFile(object):
    def __init__(self, storage):
        self.filename = _to_unicode(storage.filename)
        self.file = storage.file


class Request(object):
    def __init__(self, environ):
        self._environ = environ

    def _parse_input(self):
        def _convert(item):
            if isinstance(item, list):
                return [_to_unicode(i.value) for i in item]
            if item.filename:
                return MultipartFile(item)
            return _to_unicode(item.value)

        fs = cgi.FieldStorage(fp=self._environ['wsgi.input'],
                              environ=self._environ, keep_blank_values=True)
        inputs = {}
        for key in fs:
            inputs[key] = _convert(fs[key])  # key的value可以是一个list
        return inputs

    def _get_raw_input(self):
        if not hasattr(self, '_raw_input'):
            self._raw_input = self._parse_input()
        return self._raw_input

    def __getitem__(self, key):
        r = self._get_raw_input()[key]
        if isinstance(r, list):
            return r[0]
        return r

    def get(self, key, default=None):
        r = self._get_raw_input().get(key, default)
        if isinstance(r, list):
            return r[0]
        return r

    def gets(self, key):
        r = self._get_raw_input()[key]
        if isinstance(r, list):
            return r[:]
        return [r]
