# -*- coding: utf-8 -*-

import logging
import json
from django.db import models

from chisch.common import dependency
from chisch import curriculun_categories


logger = logging.getLogger('django')


def get_curriculum_categories():
    category_list = curriculun_categories.categories
    categories = json.dumps(category_list)
    return categories


@dependency.provider('curriculum_manager')
class CurriculumManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super(CurriculumManager, self).__init__(*args, **kwargs)
        self.categories = get_curriculum_categories()

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



