# -*- coding: utf-8 -*-

import logging
import xml.dom.minidom
from django.db import models

from chisch.common import dependency


logger = logging.getLogger('django')


def get_curriculum_category():
    first_level_types = []
    second_level_types = []
    third_level_types = []
    dom = xml.dom.minidom.parse('chisch/curriculun_categorys/internet.xml')

    first_level_type_nodes = dom.getElementsByTagName('first_level_type')
    for node in first_level_type_nodes:
        first_level_type_id = node.getAttribute('id')
        first_level_type_value = node.getAttribute('value')
        first_level_type_dict = {
            'type_id': first_level_type_id,
            'type_value': first_level_type_value
        }
        first_level_types.append(first_level_type_dict)
    second_level_type_nodes = dom.getElementsByTagName('second_level_type')
    for node in second_level_type_nodes:
        second_level_type_id = node.getAttribute('id')
        second_level_type_value = node.getAttribute('value')
        parent_level_type_id = node.parentNode.getAttribute('id')
        second_level_type_dict = {
            'id': second_level_type_id,
            'value': second_level_type_value,
            'parent_id': parent_level_type_id
        }
        second_level_types.append(second_level_type_dict)
    third_level_type_nodes = dom.getElementsByTagName('third_level_type')
    for node in third_level_type_nodes:
        third_level_type_id = node.getAttribute('id')
        third_level_type_value = node.firstChild.data
        parent_level_type_id = node.parentNode.getAttribute('id')
        third_level_type_dict = {
            'id': third_level_type_id,
            'value': third_level_type_value,
            'parent_id': parent_level_type_id
        }
        third_level_types.append(third_level_type_dict)

    result = {
        'first_level_types': first_level_types,
        'second_level_types': second_level_types,
        'third_level_types': third_level_types,
    }

    return result


@dependency.provider('curriculum_manager')
class CurriculumManager(models.Manager):

    def __init__(self, *args, **kwargs):
        super(CurriculumManager, self).__init__(*args, **kwargs)
        self.category = get_curriculum_category()

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



