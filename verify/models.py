# coding: utf-8

from django.db import models
from django.utils import timezone

from chisch.common.models import BaseModel
from .cores import VerifyManager, VerifyStatisticManager


_verify_manager = VerifyManager()
_verify_statistic_manager = VerifyStatisticManager()


class VerifyCode(BaseModel, models.Model):
    user_name = models.CharField(max_length=254)
    verify_type = models.SmallIntegerField()
    code = models.CharField(max_length=6)
    take_effect_time = models.DateTimeField()
    invalid_time = models.DateTimeField()

    manager = _verify_manager

    @property
    def is_effective(self):
        return timezone.now() <= self.invalid_time

    class Meta:
        db_table = 'verify_code'


class VerifyStatistic(BaseModel, models.Model):
    way = models.SmallIntegerField()               # 统计方式（1:user_name，2:ip）
    value = models.CharField(max_length=20)
    verify_type = models.SmallIntegerField(null=True)
    count = models.SmallIntegerField()
    last_time = models.DateTimeField(auto_now=True)

    manager = _verify_statistic_manager

    class Meta:
        db_table = 'verify_statistic'


