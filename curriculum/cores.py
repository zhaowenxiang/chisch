# -*- coding: utf-8 -*-

import logging
from django.db import models

from chisch.common import dependency


logger = logging.getLogger('django')


@dependency.provider('curriculum_manager')
class CurriculumManager(models.Manager):

    def _build_model(self, user_id, **kwargs):

        curriculum = self.model(
            user_id=user_id,
            title=kwargs['title'],
            degree=kwargs['degree'],
            brief_introduction=kwargs['brief_introduction'],
            curriculum_classification_id=kwargs['curriculum_classification_id'],
            qq_group=kwargs.get('qq_group', None),
            wx_group=kwargs.get('wx_group', None),
            cover_url=kwargs.get('cover_url', None),
            watch_person_time=0,
            star=0
        )
        return curriculum

    def create(self, user_id, **kwargs):

        curriculum = self._build_model(user_id, **kwargs)
        try:
            curriculum.save(using=self._db)
        except Exception, e:
            raise e
        return curriculum