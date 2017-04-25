# -*- coding: utf-8 -*-

import logging
import datetime

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils import timezone

from chisch.common import exceptions
from chisch.common import dependency
from chisch.common.aliservices import MnsService
from chisch.common.constents import (
    VERIFY_CODE_GET_INTERVAL,
    VERIFY_UPPER_LIMIT_BY_USER_NAME,
    VERIFY_UPPER_LIMIT_BY_IP,
    VERIFY_CODE_EFFECTIVE_TIME,
    VERIFY_TYPE_REGISTER,
    VERIFY_TYPE_LOGIN,
    VERIFY_TYPE_CHANGE_PASSWORD,
    VERIFY_TYPE_OPERATE_MAP,
    VERIFY_STATISTIC_WAY_USER_NAME,
    VERIFY_STATISTIC_WAY_IP
)
from chisch.utils import stringutils


logger = logging.getLogger('django')
mns_service = MnsService()


@dependency.provider('verify_manager')
@dependency.requires('user_manager', 'verify_statistic_manager')
class VerifyManager(models.Manager):

    def _build_model(self, user_name, verify_type):
        code = stringutils.generate_verify_code()
        take_effect_time = timezone.now()

        verify_code = self.model(
            user_name=user_name,
            verify_type=verify_type,
            code=code,
            take_effect_time=take_effect_time,
            invalid_time=take_effect_time + datetime.timedelta(
                seconds=VERIFY_CODE_EFFECTIVE_TIME)
        )
        return verify_code

    def create(self, user_name=None, verify_type=None, ip=None):
        allowed, message = self._allowed_create(user_name=user_name,
                                                verify_type=verify_type,
                                                ip=ip)
        if not allowed:
            raise exceptions.CreateVerifyCodeError(message)
        verify_code = self._build_model(user_name, verify_type)
        operate = VERIFY_TYPE_OPERATE_MAP[verify_type]
        try:
            if settings.OPEN_SSM:
                mns_service.publish_message(receiver=user_name,
                                            params={
                                               'code': verify_code.code,
                                                'operate': operate,
                                            })
            verify_code.save(using=self._db)
            self.verify_statistic_manager.create_or_update(
                user_name=user_name,
                ip=ip,
                verify_type=verify_type
            )
        except Exception:
            #TODO LOG
            raise
        return verify_code

    def _allowed_create(self, user_name, verify_type, ip):
        """判断是否允许用户获取验证码，判断依据如下
        1、当前IP今日获取验证码次数是否超过上限
        2、当前用户今日获取验证码次数是否超过上限
        3、跟上次获取同类型验证码的时间间隔是否超过指定时长
        4、如果验证码用于注册，检验该用户是否已经注册过
        5、如果验证码用于登陆、修改密码，检验用户是否已经注册过
        :param user_name:
        :param verify_type:
        :param ip:
        :return:(True or False, message)
        """
        is_registered = self.user_manager.is_registered(user_name)
        if is_registered and verify_type == VERIFY_TYPE_REGISTER:
            return False, "The user has registered."
        if not is_registered and verify_type in [VERIFY_TYPE_LOGIN,
                                                 VERIFY_TYPE_CHANGE_PASSWORD]:
            return False, "The user has not registered."

        if not settings.OPEN_MRP:
            return True, None
        else:
            return self.verify_statistic_manager.allowed_create(
                user_name=user_name,
                verify_type=verify_type,
                ip=ip
            )

    def verify(self, user_name=None, verify_type=None, code=None):
        if settings.UNIVERSAL_VERIFY_CODE and \
           code == settings.UNIVERSAL_VERIFY_CODE:
            return True
        msg = "invalid verify code."
        try:
            verify_code = self.get(user_name=user_name,
                                   verify_type=verify_type,
                                   code=code)
        except self.model.DoesNotExist:
            raise exceptions.VerifyCodeError(msg)
        if verify_code.is_effective:
            return True
        else:
            raise exceptions.VerifyCodeError(msg)


@dependency.provider('verify_statistic_manager')
class VerifyStatisticManager(models.Manager):

    def _build_model(self, way=None, value=None, verify_type=None):
        verify_statistic = self.model(way=way,
                                      value=value,
                                      verify_type=verify_type,
                                      count=1)
        return verify_statistic

    def allowed_create(self, user_name=None, verify_type=None, ip=None):
        """
        根据统计判断是否允许用户获取验证码，判断依据如下
        1、当前IP今日获取验证码次数是否超过上限
        2、当前用户今日获取验证码次数是否超过上限
        3、跟上次获取同类型验证码的时间间隔是否超过指定时长
        :param user_name:
        :param verify_type:
        :param ip:
        :return:（True or False, message)
        """
        # 当前IP今日获取验证码次数是否超过上限
        count_by_ip = self.filter(value=ip)\
                          .aggregate(Sum('count'))\
                          .get('count__sum') or 0
        if count_by_ip >= VERIFY_UPPER_LIMIT_BY_IP:
            allowed = False
            message = "Current IP verify times to reach the upper limit."
            return allowed, message

        # 当前用户今日获取验证码次数是否超过上限
        count_by_user_name = self.filter(value=user_name) \
                                 .aggregate(Sum('count')) \
                                 .get('count__sum') or 0
        if count_by_user_name > VERIFY_UPPER_LIMIT_BY_USER_NAME:
            allowed = False
            message = "Current user verify times to reach the upper limit."
            return allowed, message

        # 跟上次获取同类型验证码的时间间隔是否超过指定时长
        try:
            verify_statistic = self.get(value=user_name,
                                        verify_type=verify_type)
        except self.model.DoesNotExist:
            pass
        else:
            if timezone.now() < verify_statistic.last_time \
                    + datetime.timedelta(seconds=VERIFY_CODE_GET_INTERVAL):
                allowed = False
                message = "Frequent operation."
                return allowed, message

        return True, None

    def create_or_update(self, user_name=None, ip=None, verify_type=None):

        # 按照用户名更新统计
        try:
            verify_statistic = self.get(value=user_name,
                                        verify_type=verify_type)
        except self.model.DoesNotExist:
            verify_statistic = self._build_model(
                value=user_name,
                way=VERIFY_STATISTIC_WAY_USER_NAME,
                verify_type=verify_type
            ).save()
        else:
            verify_statistic.count += 1
            verify_statistic.save(using=self._db)

        # 按照IP更新统计
        try:
            verify_statistic = self.get(value=ip)
        except self.model.DoesNotExist:
            self._build_model(way=VERIFY_STATISTIC_WAY_IP,
                              value=ip).save()
        else:
            verify_statistic.count += 1
            verify_statistic.save(using=self._db)
