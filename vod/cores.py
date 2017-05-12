# -*- coding: utf-8 -*-

import time
import simplejson
import hashlib
import logging

from django.conf import settings

from chisch.common import exceptions
from chisch.common import http

logger = logging.getLogger('django')


def video_upload_init(api, video_name):
    vod_settings = settings.VOD
    params = {
        'api': api,
        'video_name': video_name,
        'user_unique': vod_settings['USER_UNIQUE'],
        'timestamp': str(int(time.time())),
        'format': vod_settings['RESPONSE_FORMAT'],
        'ver': vod_settings['VER'],
    }
    sign_md5 = sign(vod_settings['SECRET_KEY'], **params)
    params['sign'] = sign_md5
    url = vod_settings['URL']
    try:
        response = http.do_get(url, **params)
    except Exception, e:
        raise e
    res_body = simplejson.loads(response.read())
    if res_body['code'] == 0:
        return res_body['data']
    else:
        raise exceptions.UnexpectedError()


def sign(secret_key, **params):
    keys = sorted(params.keys())
    key_str = ''
    for key in keys:
        key_str += (key + params[key])
    key_str += secret_key
    sign_md5 = hashlib.md5(key_str)
    return sign_md5.hexdigest()

