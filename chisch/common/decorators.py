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


def lecturer_required(func):
    def wrap(_, request, *args, **kwargs):
        if request.user.is_lecturer:
            return func(_, request, *args, **kwargs)
        else:
            from chisch.common.retwrapper import RetWrapper
            from chisch.common.exceptions import NonLecturerError
            msg = ("You have not yet applied for a lecturer to prohibit "
                   "the operation.")
            return RetWrapper.wrap_and_return(NonLecturerError(msg))

    return wrap
