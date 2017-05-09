# -*- coding: utf-8 -*-

from django.db import models

from .cores import CurriculumManager
from user_.models import User

curriculum_manager = CurriculumManager()


class CurriculumClassification(models.Model):
    category = models.CharField(max_length=254)               #
    level = models.SmallIntegerField()
    superior_id = models.IntegerField(null=True)
    subordinate_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'curriculum_classification'


class Curriculum(models.Model):
    title = models.CharField(max_length=100)               # 标题
    curriculum_classification = models.ForeignKey(CurriculumClassification)
    user = models.ForeignKey(User)                         # 讲师ID
    star = models.IntegerField()                           # 好评星数
    watch_person_time = models.IntegerField()              # 观看人次
    cover_url = models.CharField(max_length=500, null=True)           # 封面URL
    degree = models.SmallIntegerField()                    # 课程程度
    created_at = models.DateTimeField(auto_now_add=True)   # 创建时间
    brief_introduction = models.TextField()                # 课程简介
    qq_group = models.CharField(max_length=20, null=True)             # qq交流群
    wx_group = models.CharField(max_length=20, null=True)             # 微信交流群

    manager = curriculum_manager

    class Meta:
        db_table = 'curriculum'

    @staticmethod
    def serializer_rule():
        return User.serializer_rule()
