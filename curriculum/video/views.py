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


@dependency.requires('video_manager', 'oss_manager')
class VideoListView(ListView):

    @login_required
    @lecturer_required
    @transaction.atomic
    def create(self, request, *args, **kwargs):

        f = kwargs.pop('files')[0] if ('files' in kwargs) \
            and len(kwargs['files']) > 0 else None

        try:
            video = self.video_manager.create(**kwargs)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        from oss.cores import get_object_key
        key = get_object_key('upload_video',
                             video.id,
                             settings.VIDEO_TYPE)
        if kwargs['price'] == 0:
            permission = oss2.OBJECT_ACL_PUBLIC_READ
        else:
            permission = oss2.OBJECT_ACL_PRIVATE

        try:
            video_url, invalid_at = self.oss_manager.single_object_upload(key, f,
                                                              permission)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        try:
            video.video_url = video_url
            video.video_url_invalid_at = invalid_at
            video.save()
        except Exception, e:
            return RetWrapper.wrap_and_return(e)
        result = _s(video, **video.serializer_rule())
        return RetWrapper.wrap_and_return(result)


@dependency.requires('curriculum_manager', 'oss_manager')
class CurriculumDetailView(DetailView):
    def update(self, request, *args, **kwargs):
        pass
