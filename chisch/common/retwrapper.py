# -*- coding: utf-8 -*-

import simplejson

from django.conf import settings
from django.http import HttpResponse

from chisch.common import exceptions


class RetWrapper(object):

    class SuccessResponse(object):
        def __init__(self):
            self.message = "success"
            self.code = 200
            self.http_status = 200

    @classmethod
    def _build_data(cls, message, http_status):
        if http_status == 200:
            return RetWrapper.SuccessResponse()
        return exceptions.UnexpectedError(message=message,
                                          http_status=http_status)

    @classmethod
    def _wrap_to_json(cls, data):

        if isinstance(data, (Exception, RetWrapper.SuccessResponse)):
            ret = {
                'status': getattr(data, 'http_status', 200),
                'code': getattr(data, 'code', 500),
                'message': getattr(data, 'message', 'Server error.'),
            }
        else:
            ret = {
                'status': 200,
                'code': 200,
                'message': 'success',
                'result': data,
            }

        content = str(ret).replace("'", '"')\
                          .replace('None', 'null')\
                          .replace('False', 'false')\
                          .replace('True', 'true')
        return content, ret['status']

    @classmethod
    def wrap_and_return(cls, data=None, **kwargs):
        if 'content_type' not in kwargs:
            kwargs['content_type'] = settings.DEFAULT_CONTENT_TYPE
        if data is None:
            data = cls._build_data(message=kwargs['message'],
                                   http_status=kwargs['http_status'])
        if kwargs['content_type'] == 'application/json':
            content, status = cls._wrap_to_json(data)
            return HttpResponse(
                content, content_type=kwargs['content_type'], status=status)
        else:
            pass
