# -*- coding: utf-8 -*-

import logging

from django.db import models
from django.db.models import Q

from chisch.common import exceptions
from chisch.common import dependency


logger = logging.getLogger('django')


@dependency.provider('work_order_manager')
class WorkOrderManager(models.Manager):

    def _build_model(self, user_id, order_type, **kwargs):
        work_order = self.model(
            user_id=user_id,
            order_type=order_type,
            status=1,
        )
        return work_order

    def create(self, user_id=None, order_type=None):
        allowed, message = self._allowed_create(user_id=user_id,
                                                order_type=order_type)
        if not allowed:
            raise exceptions.CreateWorkOrderError(message)
        work_order = self._build_model(user_id, order_type)
        try:
            work_order.save(using=self._db)
        except Exception, e:
            #TODO LOG
            raise e
        return work_order

    def _allowed_create(self, user_id, order_type, **kwargs):
        """判断是否允许用户提交工单
        1、同一用户，同类型的工单，如果存在审评中、审批通过的工单，不允许再提交
        :param user_id:
        :param type:
        :param kwargs:
        :return:(True or False, message)
        """
        work_orders_count = self.filter(
            Q(user_id=user_id) & Q(order_type=order_type), Q(status=1)).count()

        if work_orders_count > 0:
            return False, "The type of work order is already exist."
        else:
            return True, None
