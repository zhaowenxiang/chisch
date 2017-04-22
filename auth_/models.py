# coding: utf-8

from django.db import models
from django.utils import timezone

from user_.models import User
from .cores import AuthManager


_auth_manager = AuthManager()


class Token(models.Model):
    user = models.ForeignKey(User)
    access_token = models.CharField(max_length=36)
    take_effect_at = models.DateTimeField()
    invalid_at = models.DateTimeField()
    invalid_reason = models.SmallIntegerField(null=True)
    agent_idfa = models.CharField(max_length=256)

    manager = _auth_manager

    class Meta:
        db_table = 'token'

    @property
    def agent_type(self):
        return self.agent_idfa.split('-')[0]

    @property
    def agent_os(self):
        return self.agent_idfa.split('-')[1]

    @property
    def agent_id(self):
        return self.agent_idfa.split('-')[2]

    def serializer_rule(self):
        include_attr = ['access_token']
        kwargs = {
            'include_attr': include_attr,
        }
        return kwargs


