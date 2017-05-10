# -*- coding: utf-8 -*-

import logging
import json
from django.db import models

from chisch.common import dependency


logger = logging.getLogger('django')


def get_curriculum_category():
    with open('chisch/curriculun_categorys.json', 'r') as f:
        category = json.load(f)
    return category


@dependency.provider('curriculum_manager')
class CurriculumManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super(CurriculumManager, self).__init__(*args, **kwargs)
        self.category = get_curriculum_category()

    def _build_model(self, lecturer_id, **kwargs):

        curriculum = self.model(
            lecturer_id=lecturer_id,
            title=kwargs['title'],
            degree=kwargs['degree'],
            brief_introduction=kwargs['brief_introduction'],
            curriculum_type=kwargs['type'],
            qq_group=kwargs.get('qq_group', None),
            wx_group=kwargs.get('wx_group', None),
            cover_url=kwargs.get('cover_url', None),
            watch_person_time=0,
            star=0
        )
        return curriculum

    def create(self, lecturer_id, **kwargs):

        curriculum = self._build_model(lecturer_id, **kwargs)
        try:
            curriculum.save(using=self._db)
        except Exception, e:
            raise e
        return curriculum



