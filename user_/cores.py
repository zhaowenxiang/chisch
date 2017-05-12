# -*- coding: utf-8 -*-

import oss2
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import BaseUserManager
from django.db.models import Q

from chisch.common import dependency
from chisch.common import exceptions
from chisch.common.constents import (
    VERIFY_TYPE_LOGIN,
    USER_STATUS_ACTIVE,
)
from chisch.utils import stringutils


@dependency.provider('user_manager')
@dependency.requires('account_manager', 'verify_manager', 'oss_manager')
class UserManager(BaseUserManager):

    def is_registered(self, user_name):
        try:
            self.get(Q(mobile_number=user_name) | Q(email=user_name))
        except self.model.DoesNotExist:
            return False
        else:
            return True

    def _build_model(self, user_name=None, password=None):

        display_name = stringutils.hide_mobile_number(user_name)

        user = self.model(display_name=display_name,
                          mobile_number=user_name,
                          is_lecturer=False,
                          is_admin=False,
                          status=1)
        user.set_password(password)
        return user

    def create(self, user_name=None, password=None):

        if self.is_registered(user_name):
            msg = "The user has registered."
            raise exceptions.RegisterError(msg)

        user = self._build_model(user_name=user_name, password=password)
        try:
            user.save(using=self._db)
            self.account_manager.create(user=user, study_currency=0)
        except Exception, e:
            #TODO LOG
            raise e
        return user

    def auth(self, user_name, password=None, verify_type=None,
             verify_code=None):
        if password is not None:
            user, message = self._auth_by_password(user_name,
                                                   password,
                                                   verify_type)
        else:
            user, message = self._auth_by_verify_code(user_name,
                                                      verify_type,
                                                      verify_code)
        if user is None:
            raise exceptions.AuthError(message)
        return user

    def _auth_by_password(self, user_name, password, verify_type):
        user = auth.authenticate(username=user_name, password=password)
        if user is not None:
            if user.status == USER_STATUS_ACTIVE:
                return user, None
            else:
                return None, "User status exception."
        else:
            try:
                self.get(mobile_number=user_name)
            except self.model.DoesNotExist:
                return None, "The user has not registered."
            else:
                if verify_type == VERIFY_TYPE_LOGIN:
                    msg = "User name or password error."
                else:
                    msg = "Original password error."
                return None, msg

    def _auth_by_verify_code(self, user_name, verify_type, verify_code):
        try:
            self.verify_manager.verify(user_name=user_name,
                                       verify_type=verify_type,
                                       code=verify_code)
        except exceptions.VerifyCodeError:
            return None, "invalid verify code."

        user = self.get(Q(mobile_number=user_name) | Q(email=user_name))
        if user.status == USER_STATUS_ACTIVE:
            from django.conf import settings
            if "@" in user_name:
                setattr(user, 'backend',
                        settings.AUTHENTICATION_BACKENDS[1])
            else:
                setattr(user, 'backend',
                        settings.AUTHENTICATION_BACKENDS[0])
            return user, None
        else:
            return None, "User status exception."

    def update(self, user, **kwargs):
        modifiable_fields = user.modifiable_fields
        for key, value in kwargs.items():
            if key not in modifiable_fields:
                kwargs.pop(key)
            else:
                setattr(user, key, value)
        self.filter(id=user.id).update(**kwargs)
        return user

    def upload_avatar(self, user_id, f):
        from oss.cores import get_object_key
        key = get_object_key('upload_user_avatar', user_id,
                             settings.IMAGE_TYPE)
        permission = oss2.OBJECT_ACL_PUBLIC_READ
        try:
            avatar_url, _ = self.oss_manager.single_object_upload(key, f,
                                                                  permission)
        except Exception, e:
            raise e
        return avatar_url

    def detail(self, user_id):
        try:
            user = self.get(id=user_id)
        except self.model.DoesNotExist:
            raise exceptions.ResourceNotExistError(source='User')
        return user


