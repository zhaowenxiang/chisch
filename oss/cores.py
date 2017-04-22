# -*- coding: utf-8 -*-

import simplejson

import oss2
from mns.account import Account
from mns.topic import DirectSMSInfo
from mns.topic import TopicMessage

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
        assumedRoleId = sts_token_dict['AssumedRoleUser']['AssumedRoleId']
        access_key_id = sts_token_dict['Credentials']['AccessKeyId']
        access_key_secret = sts_token_dict['Credentials']['AccessKeySecret']
        security_token = sts_token_dict['Credentials']['SecurityToken']
        request_id = sts_token_dict['RequestId']
        invalid_at = timezone.now()

        sts_token = self.model(arn=arn,
                               assumedRoleId=assumedRoleId,
                               access_key_id=access_key_id,
                               access_key_secret=access_key_secret,
                               security_token=security_token,
                               request_id=request_id,
                               invalid_at=invalid_at)
        return sts_token

    def create_sts_token(self, request):

        # ALIYUN_OSS = settings.ALIYUN_OSS
        # access_key_id = ALIYUN_OSS.get('ACCESS_KEY_ID')
        # access_key_secret = ALIYUN_OSS.get('ACCESS_KEY_SECRET')
        # bucket_name = ALIYUN_OSS.get('BUCKET_NAME')
        # endpoint = ALIYUN_OSS.get('ENDPOINT')
        # role_arn = ALIYUN_OSS.get('ROLE_ARN')
        #
        # auth = oss2.Auth(access_key_id, access_key_secret)
        #
        # bucket = oss2.Bucket(auth, endpoint, bucket_name)
        # key = 'motto.txt'
        # content = 'a' * 1024 * 1024
        # filename = 'download.txt'
        #
        # # 上传文件
        # bucket.put_object(key, content)
        #
        #
        # # 创建bucket
        # # bucket = oss2.Bucket(auth, endpoint, 'test001001oifjhdk')
        # # bucket.create_bucket(oss2.BUCKET_ACL_PRIVATE)
        #
        # # sts
        # clt = client.AcsClient(access_key_id, access_key_secret, 'cn-shanghai')
        # req = AssumeRoleRequest.AssumeRoleRequest()
        #
        # req.set_accept_format('json')
        # req.set_RoleArn(role_arn)
        # req.set_RoleSessionName('oss-python-sdk-example')
        # req.set_Policy()
        #
        # sts_token_str = clt.do_action_with_exception(req)
        #
        # sts_token_dict = simplejson.loads(sts_token_str)
        #
        # sts_token = self._build_model(sts_token_dict)
        #
        # sts_token.save(using=self._db)
        #
        # return sts_token
        ALIYUN_OSS = settings.ALIYUN_OSS
        access_key_id = ALIYUN_OSS.get('ACCESS_KEY_ID')
        access_key_secret = ALIYUN_OSS.get('ACCESS_KEY_SECRET')
        bucket_name = ALIYUN_OSS.get('BUCKET_NAME')
        endpoint = ALIYUN_OSS.get('ENDPOINT')
        role_arn = ALIYUN_OSS.get('ROLE_ARN')
        my_account = Account(endpoint, access_key_id,access_key_secret)
        my_topic = my_account.get_topic('MyTopic-170418-215631')
        msg_body = "sms-message."
        direct_sms_attr = DirectSMSInfo(free_sign_name="千寻教育",
                                        template_code="SMS_62535363",
                                        single=False)
        direct_sms_attr.add_receiver(receiver="18348970617",
                                     params={
                                         "code": "409809"})

        msg = TopicMessage(msg_body, direct_sms=direct_sms_attr)
        re_msg = my_topic.publish_message(msg)
        print "Publish Message Succeed. MessageBody:%s MessageID:%s" % (
        msg_body, re_msg.message_id)
