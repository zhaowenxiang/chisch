# -*- coding: utf-8 -*-


def login_required(func):
    def wrap(_, request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(_, request, *args, **kwargs)
        else:
            from chisch.common.retwrapper import RetWrapper
            from chisch.common.exceptions import LoggedOffError
            msg = "The user has not login."
            return RetWrapper.wrap_and_return(LoggedOffError(msg))

    return wrap
