# -*- coding: utf-8 -*-

import logging

from chisch.common.retwrapper import RetWrapper
import cores


logger = logging.getLogger('django')


def video_upload_init(request):
    params = request.GET
    api = params['api']
    video_name = params['video_name']
    try:
        resp_data = cores.video_upload_init(api, video_name)
    except Exception, e:
        return RetWrapper.wrap_and_return(e)
    return RetWrapper.wrap_and_return(resp_data)
