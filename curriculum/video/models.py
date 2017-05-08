# -*- coding: utf-8 -*-

from django.db import models

from .cores import VideoManager
from user_.models import User
from curriculum.models import Curriculum

video_manager = VideoManager()


class Video(models.Model):
    curriculum = models.ForeignKey(Curriculum)             # 所属课程
    chapter = models.SmallIntegerField()                   # 章
    hour = models.SmallIntegerField()                      # 课时
    title = models.CharField(max_length=100)               # 标题
    duration = models.CharField(max_length=5)              # 时长
    price = models.IntegerField()                          # 价格
    try_see_duration = models.SmallIntegerField()          # 试看时间
    video_url = models.CharField(max_length=500, null=True)  # 视频地址
    video_url_invalid_at = models.DateTimeField(null=True)   # 视频url失效时间
    status = models.SmallIntegerField()                    # 视频状态
    created_at = models.DateTimeField(auto_now_add=True)   # 创建时间
    updated_at = models.DateTimeField(auto_now=True)       # 修改时间

    manager = video_manager

    class Meta:
        db_table = 'video'

    @staticmethod
    def serializer_rule():
        return User.serializer_rule()
