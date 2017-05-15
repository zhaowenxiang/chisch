# -*- coding: utf-8 -*-

import json
from aliyunsdkvod.request.v20170321 import CreateUploadVideoRequest
from aliyunsdkcore import client
from django.conf import settings


def create_upload_video(clt):
    request = CreateUploadVideoRequest.CreateUploadVideoRequest()
    request.set_accept_format('JSON')
    request.set_Title("test_upload")
    request.set_FileName("test_upload.mov")
    request.set_FileSize(1024L)
    request.set_Description("test_decription")
    # request.set_CoverURL("test_url")
    response = json.loads(clt.do_action_with_exception(request))
    return response
#
# import sys
# import os
# import urllib,urllib2
# import base64
# import hmac
# import hashlib
# from hashlib import sha1
# import time
# import uuid
# import json
# from django.conf import settings
#
# vod_settings = settings.VOD
#
# user_params = {'Action': 'SingleSendSms', 'ParamString': '', 'RecNum': '13881780579','SignName': '','TemplateCode': 'xx' }
#
#
# def get_public_params():
#     timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
#     kwargs = {
#         'Format': vod_settings['FORMAT'],
#         'Version': vod_settings['VERSION'],
#         'AccessKeyId': vod_settings['ACCESS_KEY_ID'],
#         'SignatureMethod': vod_settings['SIGNATUREMETHOD'],
#         'SignatureVersion': vod_settings['SIGNATUREVERSION'],
#         'SignatureNonce': str(uuid.uuid1()),
#         'Timestamp': timestamp
#     }
#     return kwargs
#
#
# def percent_encode(encode_str):
#     encode_str = str(encode_str)
#     res = urllib.quote(encode_str.decode('utf8').encode('utf8'), '')
#     res = res.replace('+', '%20')
#     res = res.replace('*', '%2A')
#     res = res.replace('%7E', '~')
#     return res
#
#
# def compute_signature(access_key_secret, **params):
#     keys = sorted(params.keys())
#     canonicalized_query_str = ''
#     for key in keys:
#         canonicalized_query_str += '&' + percent_encode(
#             key) + '=' + percent_encode(params[key])
#     string_to_sign = 'GET&%2F&' + percent_encode(canonicalized_query_str[1:])
#     print "stringToSign:  " + string_to_sign
#     h = hmac.new(access_key_secret + "&", string_to_sign, sha1)
#     signature = base64.encodestring(h.digest()).strip()
#     return signature
#
#
# def compose_url(**params):
#     public_params = get_public_params()
#     params.update(public_params)
#     access_key_secret = vod_settings['SECRET_KEY']
#     signature = compute_signature(access_key_secret, **params)
#     params['Signature'] = signature
#     url = vod_settings['SERVER_URL'] + "/?" + urllib.urlencode(params)
#     return url
#
#
# def make_request(user_params, quiet=False):
#     url = compose_url(user_params)
#     request = urllib2.Request(url)
#     try:
#         conn = urllib2.urlopen(request)
#         response = conn.read()
#     except urllib2.HTTPError, e:
#         print(e.read().strip())
#     try:
#         obj = json.loads(response)
#         if quiet:
#             return obj
#     except ValueError, e:
#         raise SystemExit(e)
#     json.dump(obj, sys.stdout, sort_keys=True, indent=2)
#     sys.stdout.write('\n')
#
#
def get_url():
    vod_settings = settings.VOD
    clt = client.AcsClient(vod_settings['ACCESS_KEY_ID'],
                           vod_settings['SECRET_KEY'],
                           'cn-shanghai')
    res = create_upload_video(clt)
    return res
