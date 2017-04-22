# -*- coding: utf-8 -*-

from django.db import models

from chisch.common import dependency


@dependency.provider('account_manager')
class AccountManager(models.Manager):
    pass

    # def build_model(self, user_id=None):
    #     account = self.model(user_id=user_id, study_currency=0)
    #     return account
