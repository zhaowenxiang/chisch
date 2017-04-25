# -*- coding: utf-8 -*-

"""
Django local_settings for chisch project.
import by 'setting.py.
"""

# Open malicious authentication
OPEN_MRP = False
OPEN_SSM = False

# The name of the certificate
ACCESS_TOKEN_NAME = 'Access-Token'

# universal verify code
UNIVERSAL_VERIFY_CODE = "888888"

ALIYUN_OSS = {
    'BUCKET_NAME': 'chisch',
    'ACCESS_KEY_ID': 'LTAInczWIrr8Xjdb',
    'ACCESS_KEY_SECRET': 'oDV6sIMkJsDCb24PgQNAoLWACefYae',
    'ENDPOINT': 'https://oss-cn-shenzhen.aliyuncs.com',
    'ROLE_ARN': 'acs:ram::1709927201743129:role/aliyunosstokengeneratorrole',
    'TokenExpireTime': 60 * 60,
    'REGION': 'cn-shenzhen',
    'FILE_PATH':[
        {'purpose': 'upload_avatar', 'path': '/image/user/avatar/'},
        {'purpose': 'upload_video', 'path': '/image/user/video/'}
    ]
}

MNS = {
    'ACCESS_KEY_ID': 'LTAIFSaBApB2TuC4',
    'ACCESS_KEY_SECRET': '0qMu5s3yHEBrxb2klSyZKnHmOPb0HZ',
    'ENDPOINT': 'https://1709927201743129.mns.cn-hangzhou.aliyuncs.com/',
    'SIGN_NAME': '千寻教育',
    'TEMPLATE_CODE': 'SMS_62440527',
    'TOPIC': 'sms.topic-cn-hangzhou',
    'QUEUE_NAME': 'verify-code-queue',
}

