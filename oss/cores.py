# -*- coding: utf-8 -*-

import oss2
import simplejson

from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
from django.conf import settings
from django.db import models
from django.utils import timezone

from chisch.common import dependency

def _set_sts_token_extra_info(sts_token):
    ALIYUN_OSS = settings.ALIYUN_OSS
    bucket_name = ALIYUN_OSS.get('BUCKET_NAME')
    file_paths = ALIYUN_OSS.get('FILE_PATH')
    for file_path in file_paths:
        if file_path.get('purpose', None) == sts_token.purpose:
            path = file_path.get('path')
            name = '1' + '.png'
            break
    object_key = path + name
    setattr(sts_token, 'backup_name', bucket_name)
    setattr(sts_token, 'object_key', object_key)
    return sts_token


@dependency.provider('oss_manager')
class OssManager(models.Manager):

    def _build_model(self, sts_token_dict, purpose=None):
        arn = sts_token_dict['AssumedRoleUser']['Arn']
        assumed_role_id = sts_token_dict['AssumedRoleUser']['AssumedRoleId']
        access_key_id = sts_token_dict['Credentials']['AccessKeyId']
        access_key_secret = sts_token_dict['Credentials']['AccessKeySecret']
        security_token = sts_token_dict['Credentials']['SecurityToken']
        expiration_str = sts_token_dict['Credentials']['Expiration']
        expiration_timestamp = oss2.utils.to_unixtime(expiration_str,
                                                      '%Y-%m-%dT%H:%M:%SZ')
        expiration = timezone.datetime.fromtimestamp(expiration_timestamp)

        sts_token = self.model(arn=arn,
                               assumed_role_id=assumed_role_id,
                               access_key_id=access_key_id,
                               access_key_secret=access_key_secret,
                               security_token=security_token,
                               purpose=purpose,
                               expiration=expiration)
        return sts_token

    def get_sts_token(self, purpose):
        try:
            sts_token = self.get(purpose=purpose)
        except self.model.DoesNotExist:
            sts_token = self._create_sts_token(purpose)
        finally:
            if not sts_token.is_effective:
                sts_token.delete()
                sts_token = self._create_sts_token(purpose)
        sts_token = _set_sts_token_extra_info(sts_token)
        return sts_token


    def _create_sts_token(self, purpose):

        ALIYUN_OSS = settings.ALIYUN_OSS
        access_key_id = ALIYUN_OSS.get('ACCESS_KEY_ID')
        access_key_secret = ALIYUN_OSS.get('ACCESS_KEY_SECRET')
        role_arn = ALIYUN_OSS.get('ROLE_ARN')
        region = ALIYUN_OSS.get('REGION')
        duration_seconds = ALIYUN_OSS.get('TokenExpireTime')
        bucket_name = ALIYUN_OSS.get('BUCKET_NAME')

        clt = client.AcsClient(access_key_id, access_key_secret, region)
        req = AssumeRoleRequest.AssumeRoleRequest()

        req.set_accept_format('json')
        req.set_RoleArn(role_arn)
        req.set_RoleSessionName('chisch')
        req.set_DurationSeconds(duration_seconds)

        try:
            sts_token_str = clt.do_action_with_exception(req)
        except Exception, e:
            raise e

        sts_token_dict = simplejson.loads(sts_token_str)

        sts_token = self._build_model(sts_token_dict, purpose='upload_avatar')

        sts_token.save(using=self._db)


        return sts_token
