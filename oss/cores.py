# -*- coding: utf-8 -*-

import oss2
import simplejson

from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest
from django.conf import settings
from django.db import models
from django.utils import timezone

from chisch.common import dependency


@dependency.provider('oss_manager')
class OssManager(models.Manager):

    def _build_model(self, sts_token_dict):
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
                               expiration=expiration)
        return sts_token

    def create_sts_token(self, request):

        ALIYUN_OSS = settings.ALIYUN_OSS
        access_key_id = ALIYUN_OSS.get('ACCESS_KEY_ID')
        access_key_secret = ALIYUN_OSS.get('ACCESS_KEY_SECRET')
        role_arn = ALIYUN_OSS.get('ROLE_ARN')
        region = ALIYUN_OSS.get('REGION')
        endpoint = ALIYUN_OSS.get('ENDPOINT')
        duration_seconds = ALIYUN_OSS.get('TokenExpireTime')
        bucket_name = ALIYUN_OSS.get('BUCKET_NAME')
        role_arn = ALIYUN_OSS.get('ROLE_ARN')

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

        sts_token = self._build_model(sts_token_dict)

        sts_token.save(using=self._db)
        setattr(sts_token, 'backup_name', bucket_name)
        setattr(sts_token, 'object_key', '1.png')

        auth = oss2.StsAuth(sts_token.access_key_id,
                         sts_token.access_key_secret,
                         sts_token.security_token)

        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        bucket.put_object('motto.txt', 'Never give up. - Jack Ma')
        return sts_token
