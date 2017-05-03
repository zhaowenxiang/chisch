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
    def serializer_rule():
        """
        序列化规则
        :return:
        """
        extra_attr = ['account']
        exclude_attr = ['password', 'backend']
        kwargs = {
            'extra_attr': extra_attr,
            'exclude_attr': exclude_attr,
        }
        return kwargs

    @property
    def un_modifiable_fields(self):
        return ['id', 'password', 'mobile_number', 'email',
                'created_at', 'updated_at', 'last_login',
                'is_lecturer', 'is_admin', 'status']

