# coding: utf-8

from django.db import models
from django.utils import timezone

from chisch.common.models import BaseModel
from user_.models import User
from .cores import WorkOrderManager


_work_order__manager = WorkOrderManager()


class WorkOrder(BaseModel, models.Model):
    user = models.ForeignKey(User, null=True)                           # 提交用户
    order_type = models.SmallIntegerField()                        # 工单类型
    created_at = models.DateTimeField(auto_now_add=True)     # 提交时间
    status = models.SmallIntegerField()                      # 工单状态
    # 审批人
    approver = models.ForeignKey(User, null=True, related_name='approver')
    reject_reason = models.CharField(max_length=200, null=True)       # 拒绝原因

    manager = _work_order__manager

    class Meta:
        db_table = 'work_order'

    @classmethod
    def serializer_rule(cls, own=True):
        kwargs = super(WorkOrder, cls).serializer_rule()
        kwargs.update({
            'foreign': ['user']
        })
        return kwargs
