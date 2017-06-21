# -*- coding: utf-8 -*-

import logging

import oss2
from django.conf import settings
from django.db import transaction

from chisch.common import dependency
from chisch.common.decorators import login_required, lecturer_required
from chisch.common.retwrapper import RetWrapper
from chisch.common.serializer import s as _s
from chisch.common.views import DetailView, ListView


logger = logging.getLogger('django')


@dependency.requires('curriculum_manager')
class CurriculumCategoryListView(ListView):
    def get(self, request):
        result = self.curriculum_manager.category
        return RetWrapper.wrap_and_return(result)


@dependency.requires('curriculum_manager', 'oss_manager')
class CurriculumListView(ListView):

    @login_required
    @lecturer_required
    @transaction.atomic
    def create(self, request, *args, **kwargs):

        lecturer_id = request.user.id

        f = kwargs.pop('files')[0] if ('files' in kwargs) \
            and len(kwargs['files']) > 0 else None

        try:
            curriculum = self.curriculum_manager.create(lecturer_id=lecturer_id,
                                                        **kwargs)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        if f:
            from oss.cores import get_object_key
            key = get_object_key('create_curriculum',
                                 curriculum.id,
                                 settings.IMAGE_TYPE)
            permission = oss2.OBJECT_ACL_PUBLIC_READ
            try:
                cover_url, _ = self.oss_manager.single_object_upload(key, f,
                                                                  permission)
            except Exception, e:
                return RetWrapper.wrap_and_return(e)
            try:
                curriculum.cover_url = cover_url
                curriculum.save()
            except Exception, e:
                return RetWrapper.wrap_and_return(e)
        result = _s(curriculum, own=True)
        return RetWrapper.wrap_and_return(result)

    def page_list(self, request, *args, **kwargs):
        page_size = kwargs['page_size']
        page_number = kwargs['page_number']
        offset = (page_number-1) * page_size
        limit = offset + page_size
        try:
            curriculums = self.curriculum_manager.all()[offset: limit]
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        result = {}
        result['rows'] = _s(curriculums, own=True)
        result['pagination'] = {
            'total': 55,
        }
        return RetWrapper.wrap_and_return(result)

    def get_curriculum_categories(self, request, *args, **kwargs):
        try:
            category = self.curriculum_manager.get_curriculum_categories()
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        return RetWrapper.wrap_and_return(category)


@dependency.requires('curriculum_manager', 'oss_manager')
class CurriculumDetailView(DetailView):
    def update(self, request, *args, **kwargs):
        pass
