# -*- coding: utf-8 -*-

import logging

from chisch.common.constents import (
    TOKEN_INVALID_REASON_UNRECOGNIZED as tiru,
    TOKEN_INVALID_REASON_EXPIRE as tire,
    TOKEN_INVALID_REASON_LOGIN_OTHER_PLACE as tirliop,
)

LOG = logging.getLogger(__name__)

# Tests use this to make exception message format errors fatal
_FATAL_EXCEPTION_FORMAT_ERRORS = False


def _format_with_kwargs(msg_format, kwargs):
    try:
        return msg_format % kwargs
    except UnicodeDecodeError:
        try:
            pass
        except UnicodeDecodeError:
            # NOTE(jamielennox): This is the complete failure case
            # at least by showing the template we have some idea
            # of where the error is coming from
            return msg_format

        return msg_format % kwargs


class Error(Exception):
    """Base error class.
    Child classes should define an HTTP status code, title, and a
    message_format.
    """

    http_status = 200
    code = None
    message_format = None

    def __init__(self, message=None, **kwargs):
        try:
            message = self._build_message(message, **kwargs)
        except KeyError:
            if _FATAL_EXCEPTION_FORMAT_ERRORS:
                raise
            else:
                LOG.warning('missing exception kwargs (programmer error)')
                message = self.message_format

        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):
        """Build and returns an exception message.
        :raises KeyError: given insufficient kwargs
        """
        if message:
            return message
        return _format_with_kwargs(self.message_format, kwargs)


class UnexpectedError(Error):
    code = 500


class Error400(Error):
    """
    Bad Request
    1、语义有误，当前请求无法被服务器理解。除非进行修改，否则客户端不应该重复提交这个请求。
    2、请求参数有误。
    """
    pass


class Error401(Error):
    """
    Unauthorized
    当前请求需要用户验证。该响应必须包含一个适用于被请求资源的 WWW-Authenticate 信息头用以询
    问用户信息。客户端可以重复提交一个包含恰当的 Authorization 头信息的请求。如果当前请求已经
    包含了 Authorization 证书，那么401响应代表着服务器验证已经拒绝了那些证书。如果401响应包
    含了与前一个响应相同的身份验证询问，且浏览器已经至少尝试了一次验证，那么浏览器应当向用户展示
    响应中包含的实体信息，因为这个实体信息中可能包含了相关诊断信息
    """
    pass


class Error402(Error):
    """
    Payment Required
    该状态码是为了将来可能的需求而预留的。
    """
    pass


class Error403(Error):
    """
    Forbidden
    服务器已经理解请求，但是拒绝执行它。与401响应不同的是，身份验证并不能提供任何帮助，而且这个请
    求也不应该被重复提交。如果这不是一个 HEAD 请求，而且服务器希望能够讲清楚为何请求不能被执行，
    那么就应该在实体内描述拒绝的原因。当然服务器也可以返回一个404响应，假如它不希望让客户端获得任
    何信息。
    """


class Error404(Error):
    """
    Not Found
    请求失败，请求所希望得到的资源未被在服务器上发现。没有信息能够告诉用户这个状况到底是暂时的还是
    永久的。假如服务器知道情况的话，应当使用410状态码来告知旧资源因为某些内部的配置机制问题，已经
    永久的不可用，而且没有任何可以跳转的地址。404这个状态码被广泛应用于当服务器不想揭示到底为何请
    求被拒绝或者没有其他适合的响应可用的情况下。出现这个错误的最有可能的原因是服务器端没有这个页面
    。
    """


class Error405(Error):
    """
    Method Not Allowed
    请求行中指定的请求方法不能被用于请求相应的资源。该响应必须返回一个Allow 头信息用以表示出当前
    资源能够接受的请求方法的列表。
    鉴于 PUT，DELETE 方法会对服务器上的资源进行写操作，因而绝大部分的网页服务器都不支持或者在默
    认配置下不允许上述请求方法，对于此类请求均会返回405错误。
    """


class Error406(Error):
    """
    Not Acceptable
    请求的资源的内容特性无法满足请求头中的条件，因而无法生成响应实体。
    """


class CreateVerifyCodeError(Error403):
    code = 40301


class RegisterError(Error403):
    code = 40302


class AuthError(Error403):
    code = 40303


class ChangePasswordError(Error403):
    code = 40304


class LoggedOffError(Error403):
    code = 40305


class VerifyCodeError(Error403):
    code = 40306


class NonLecturerError(Error403):
    code = 40307


class ResourceNotExistError(Error404):
    code = 40401
    message_format = "%(source)s does not exist."


class InvalidAccessTokenErr(Error401):

    def _build_message(self, message, **kwargs):

        reason = kwargs.get('reason', None)

        if reason == tiru:
            self.code = 40100
            return "The access token is unrecognized."
        elif reason == tire:
            self.code = 40101
            return "The access token has expired."
        elif reason == tirliop:
            self.code = 40102
            return "The user has login in other place."
