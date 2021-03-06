# -*- coding: utf-8 -*-
from django.db import models

from user_.models import User
from .cores import AccountManager
from chisch.common.models import BaseModel

# Create your models here.


_account_manager = AccountManager()


class Account(BaseModel, models.Model):
    user = models.OneToOneField(User)
    study_currency = models.PositiveIntegerField()

    manager = _account_manager

    class Meta:
        db_table = 'account'
