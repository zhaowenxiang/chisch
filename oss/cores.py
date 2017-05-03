# -*- coding: utf-8 -*-

#
# import oss2
# import simplejson
#
# from aliyunsdkcore import client
# from aliyunsdksts.request.v20150401 import AssumeRoleRequest
# from django.conf import settings
# from django.db import models
# from django.utils import timezone
#
# from chisch.common import dependency
#
#
# def _set_sts_token_extra_info(sts_token,
#                               purpose,
#                               attached_object_id):
#     ALIYUN_OSS = settings.ALIYUN_OSS
#     bucket_name = ALIYUN_OSS.get('BUCKET_NAME')
#     endpoint = ALIYUN_OSS.get('ENDPOINT')
#     object_keys_sub_element = ALIYUN_OSS.get('OBJECT_KEYS_SUB_ELEMENT')
#     object_key_sub_element = object_keys_sub_element.get(purpose)
#
#     path = object_key_sub_element['path']
#     key_suffix = object_key_sub_element['key_suffix']
#     number = object_key_sub_element['number']
#
#     if number == 'one':
#         object_key = path + attached_object_id + key_suffix
#     else:
#         object_key = path + attached_object_id + '-*' + key_suffix
#
#     setattr(sts_token, 'backup_name', bucket_name)
#     setattr(sts_token, 'object_key', object_key)
#     setattr(sts_token, 'endpoint', endpoint)
#     return sts_token
#
#
# @dependency.provider('oss_manager')
# class OssManager(models.Manager):
#
#     # def _build_model(self, sts_token_dict, purpose=None):
#     #     arn = sts_token_dict['AssumedRoleUser']['Arn']
#     #     assumed_role_id = sts_token_dict['AssumedRoleUser']['AssumedRoleId']
#     #     access_key_id = sts_token_dict['Credentials']['AccessKeyId']
#     #     access_key_secret = sts_token_dict['Credentials']['AccessKeySecret']
#     #     security_token = sts_token_dict['Credentials']['SecurityToken']
#     #     expiration_str = sts_token_dict['Credentials']['Expiration']
#     #     expiration_timestamp = oss2.utils.to_unixtime(expiration_str,
#     #                                                   '%Y-%m-%dT%H:%M:%SZ')
#     #     expiration = timezone.datetime.fromtimestamp(expiration_timestamp)
#     #
#     #     sts_token = self.model(arn=arn,
#     #                            assumed_role_id=assumed_role_id,
#     #                            access_key_id=access_key_id,
#     #                            access_key_secret=access_key_secret,
#     #                            security_token=security_token,
#     #                            purpose=purpose,
#     #                            expiration=expiration)
#     #     return sts_token
#     #
#     # def get_sts_token(self, purpose, attached_object_id):
#     #     try:
#     #         sts_token = self.get(purpose=purpose)
#     #     except self.model.DoesNotExist:
#     #         sts_token = self._create_sts_token(purpose)
#     #     finally:
#     #         if not sts_token.is_effective:
#     #             sts_token.delete()
#     #             sts_token = self._create_sts_token(purpose)
#     #     sts_token = _set_sts_token_extra_info(sts_token,
#     #                                           purpose,
#     #                                           attached_object_id)
#     #     return sts_token
#     #
#     # def _create_sts_token(self, purpose):
#     #
#     #     ALIYUN_OSS = settings.ALIYUN_OSS
#     #     access_key_id = ALIYUN_OSS.get('ACCESS_KEY_ID')
#     #     access_key_secret = ALIYUN_OSS.get('ACCESS_KEY_SECRET')
#     #     role_arn = ALIYUN_OSS.get('ROLE_ARN')
#     #     region = ALIYUN_OSS.get('REGION')
#     #     duration_seconds = ALIYUN_OSS.get('TokenExpireTime')
#     #
#     #     clt = client.AcsClient(access_key_id, access_key_secret, region)
#     #     req = AssumeRoleRequest.AssumeRoleRequest()
#     #
#     #     req.set_accept_format('json')
#     #     req.set_RoleArn(role_arn)
#     #     req.set_RoleSessionName('chisch')
#     #     req.set_DurationSeconds(duration_seconds)
#     #
#     #     try:
#     #         sts_token_str = clt.do_action_with_exception(req)
#     #     except Exception, e:
#     #         raise e
#     #     sts_token_dict = simplejson.loads(sts_token_str)
#     #     sts_token = self._build_model(sts_token_dict, purpose=purpose)
#     #     sts_token.save(using=self._db)
#     #     return sts_token


import time
import datetime
import json
import base64
import hmac
import hashlib
import os
import crcmod
import requests

from chisch.common import dependency
from django.conf import settings

# from django.conf import settings

# 以下代码展示了PostObject的用法。PostObject不依赖于OSS Python SDK。

# POST表单域的详细说明请参RFC2388 https://tools.ietf.org/html/rfc2388
# PostObject的官网 https://help.aliyun.com/document_detail/31988.html
# PostObject错误及排查 https://yq.aliyun.com/articles/58524


def calculate_crc64(data):
    """计算文件的MD5
    :param data: 数据
    :return 数据的MD5值
    """
    _POLY = 0x142F0E1EBA9EA3693
    _XOROUT = 0XFFFFFFFFFFFFFFFF

    crc64 = crcmod.Crc(_POLY, initCrc=0, xorOut=_XOROUT)
    crc64.update(data)

    return crc64.crcValue


def build_gmt_expired_time(expire_time):
    """生成GMT格式的请求超时时间
    :param int expire_time: 超时时间，单位秒
    :return str GMT格式的超时时间
    """
    now = int(time.time())
    expire_syncpoint = now + expire_time

    expire_gmt = datetime.datetime.fromtimestamp(expire_syncpoint).isoformat()
    expire_gmt += 'Z'

    return expire_gmt


def build_encode_policy(expired_time, condition_list):
    """生成policy
    :param int expired_time: 超时时间，单位秒
    :param list condition_list: 限制条件列表
    """
    policy_dict = {
        'expiration': build_gmt_expired_time(expired_time),
        'conditions': condition_list
    }

    policy = json.dumps(policy_dict).strip()
    policy_encode = base64.b64encode(policy)

    return policy_encode


def build_signature(access_key_secret, encode_policy):
    """生成签名
    :param str access_key_secret: access key secret
    :param str encode_policy: 编码后的Policy
    :return str 请求签名
    """
    h = hmac.new(access_key_secret, encode_policy, hashlib.sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature


def bulid_callback(cb_url, cb_body, cb_body_type=None, cb_host=None):
    """生成callback字符串
    :param str cb_url: 回调服务器地址，文件上传成功后OSS向此url发送回调请求
    :param str cb_body: 发起回调请求的Content-Type，默认application/x-www-form-urlencoded
    :param str cb_body_type: 发起回调时请求body
    :param str cb_host: 发起回调请求时Host头的值
    :return str 编码后的Callback
    """
    callback_dict = {
        'callbackUrl': cb_url,
        'callbackBody': cb_body,
    }

    if cb_body_type is None:
        callback_dict['callbackBodyType'] = 'application/x-www-form-urlencoded'
    else:
        callback_dict['callbackBodyType'] = cb_body_type

    if cb_host is not None:
        callback_dict['callbackHost'] = cb_host

    callback_param = json.dumps(callback_dict).strip()
    base64_callback = base64.b64encode(callback_param);

    return base64_callback


def build_post_url(endpoint, bucket_name):
    """生成POST请求URL
    :param str endpoint: endpoint
    :param str bucket_name: bucket name
    :return str POST请求URL
    """
    if endpoint.startswith('http://'):
        return endpoint.replace('http://', 'http://{0}.'.format(bucket_name))
    elif endpoint.startswith('https://'):
        return endpoint.replace('https://', 'https://{0}.'.format(bucket_name))
    else:
        return 'http://{0}.{1}'.format(bucket_name, endpoint)


def build_post_body(field_dict, boundary):
    """生成POST请求Body
    :param dict field_dict: POST请求表单域
    :param str boundary: 表单域的边界字符串
    :return str POST请求Body
    """
    post_body = b''

    # 编码表单域
    for k, v in field_dict.iteritems():
        if k != 'content' and k != 'content-type':
            post_body += '''--{0}\r\nContent-Disposition: form-data; name=\"{1}\"\r\n\r\n{2}\r\n'''.format(
                boundary, k, v)

    # 上传文件的内容，必须作为最后一个表单域
    post_body += '''--{0}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{1}\"\r\nContent-Type: {2}\r\n\r\n{3}'''.format(
        boundary, field_dict['key'], field_dict['content-type'],
        field_dict['content'])

    # 加上表单域结束符
    post_body += '\r\n--{0}--\r\n'.format(boundary)

    return post_body


def build_post_headers(body_len, boundary, headers=None):
    """生气POST请求Header
    :param str body_len: POST请求Body长度
    :param str boundary: 表单域的边界字符串
    :param dict 请求Header
    """
    headers = headers if headers else {}
    headers['Content-Length'] = str(body_len)
    headers['Content-Type'] = 'multipart/form-data; boundary={0}'.format(
        boundary)

    return headers


def get_object_key(action, attachment_id, file_suffix):
    aliyun_oss = settings.ALIYUN_OSS
    key_sub_elements = aliyun_oss['OBJECT_KEYS_SUB_ELEMENTS'][action]
    if key_sub_elements.get('only_one', False):
        key = key_sub_elements['path'] + str(attachment_id) + file_suffix
        return key
    else:
        pass


@dependency.provider('oss_manager')
class OssManager(object):

    def __init__(self):
        # 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
        # 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
        ALIYUN_OSS = settings.ALIYUN_OSS
        self.access_key_id = ALIYUN_OSS.get('ACCESS_KEY_ID')
        self.access_key_secret = ALIYUN_OSS.get('ACCESS_KEY_SECRET')
        self.bucket_name = ALIYUN_OSS.get('BUCKET_NAME')
        self.endpoint = ALIYUN_OSS.get('ENDPOINT')
        self.boundary = ALIYUN_OSS.get('BOUNDARY')


    def get_object_url(self):
        pass

    def single_object_direct_upload(self, key, f):
        """
        :param key: Object name for cloud storage
        :param f: The file
        :return: status
        """
        # POST请求表单域，注意大小写
        policy = build_encode_policy(120,
                                     [
                                         ['eq', '$bucket', self.bucket_name],
                                         ['content-length-range', 0, 104857600]
                                     ])
        field_dict = {
            'OSSAccessKeyId': self.access_key_id,
            # Policy包括超时时间(单位秒)和限制条件condition
            'policy': policy,
            'Signature': build_signature(self.access_key_secret, policy),
            'Content-Disposition': 'attachment;filename=' + key,
            'key': key,
            'content-type': 'image/png',
            'content': f['value'],
        }
        body = build_post_body(field_dict, self.boundary)
        headers = build_post_headers(len(body), self.boundary)
        try:
            resp = requests.post(build_post_url(self.endpoint,
                                                self.bucket_name),
                                 data=body,
                                 headers=headers)
        except Exception, e:
            raise e
        return resp

# # 确认请求结果
# assert resp.status_code == 200
# assert resp.content == '{"Status":"OK"}'
# assert resp.headers['x-oss-hash-crc64ecma'] == str(
#     calculate_crc64(field_dict['content']))

