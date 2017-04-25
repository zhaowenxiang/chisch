# coding: utf-8

from django.db import models
from django.utils import timezone
from .cores import OssManager


_oss_manager = OssManager()


class StsToken(models.Model):
    arn = models.CharField(max_length=500)
    assumed_role_id = models.CharField(max_length=500)
    access_key_id = models.CharField(max_length=500)
    access_key_secret = models.CharField(max_length=500)
    security_token = models.TextField()
    purpose = models.CharField(max_length=100)
    expiration = models.DateTimeField()

    manager = _oss_manager

    class Meta:
        db_table = 'sts_token'

    @property
    def is_effective(self):
        return timezone.now() <= self.expiration


