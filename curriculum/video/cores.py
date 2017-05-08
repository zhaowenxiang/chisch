# -*- coding: utf-8 -*-

import logging
from django.db import models

from chisch.common.constents import (
    VIDEO_STATUS_NORMAL as vtn,
    VIDEO_STATUS_ABNORMAL as vsan,
)
from chisch.common import dependency


logger = logging.getLogger('django')


@dependency.provider('video_manager')
class VideoManager(models.Manager):

    def _build_model(self, **kwargs):

        video = self.model(
            curriculum_id=kwargs['curriculum_id'],
            chapter=kwargs['chapter'],
            hour=kwargs['hour'],
            title=kwargs['title'],
            duration=kwargs['duration'],
            price=kwargs['price'],
            try_see_duration=kwargs['try_see_duration'],
            status=vtn,
        )
        return video

    def create(self, **kwargs):
        video = self._build_model(**kwargs)
        try:
            video.save(using=self._db)
        except Exception, e:
            raise e
        return video

    def update(self, **kwargs):
        pass