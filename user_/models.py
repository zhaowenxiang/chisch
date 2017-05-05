# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from chisch.common.models import BaseModel
from .cores import UserManager

# Create your models here.

_user_manager = UserManager()


class User(BaseModel, AbstractBaseUser):
    display_name = models.CharField(max_length=254,
                                    null=True)
    mobile_number = models.CharField(max_length=11,
                                     null=True,
                                     unique=True)
    email = models.EmailField(max_length=254,
                              null=True,
                              unique=True)
    avatar_url = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=1, null=True)
    date_of_birth = models.CharField(max_length=10, null=True)
    education = models.SmallIntegerField(null=True)
    favorite = models.CharField(max_length=18, null=True)
    city = models.CharField(max_length=255, null=True)
    is_lecturer = models.BooleanField()
    is_admin = models.BooleanField()
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'mobile_number'

    manager = _user_manager

    class Meta:
        db_table = 'user'

    @staticmethod
    def serializer_rule(user_id=None, token_user_id=None, own=False):
        """
        序列化规则，根据user_id以及token_user_id判断发起操作的用户跟被操作
        用户是否是同一个用户，不同的情况，序列化的规则不同。例如，用户自己可以
        看到自己的账户信息，但是对外展示的时候要隐藏账户信息
        :param user_id:
        :param token_user_id:
        :return: kwargs
        """
        extra_attr = []
        exclude_attr = ['password', 'backend']
        if user_id == token_user_id:
            extra_attr += ['account']
            kwargs = {
                'extra_attr': extra_attr,
                'exclude_attr': exclude_attr,
            }
            return kwargs
        else:
            kwargs = {
                'exclude_attr': exclude_attr + ['created_at', 'updated_at',
                                                'mobile_number', 'email',
                                                'is_admin'],
            }
            return kwargs

    @property
    def un_modifiable_fields(self):
        return ['id', 'password', 'mobile_number', 'email',
                'created_at', 'updated_at', 'last_login',
                'is_lecturer', 'is_admin', 'status']

