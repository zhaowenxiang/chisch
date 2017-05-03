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
    'ACCESS_KEY_ID': 'LTAIFSaBApB2TuC4',
    'ACCESS_KEY_SECRET': '0qMu5s3yHEBrxb2klSyZKnHmOPb0HZ',
    'ENDPOINT': 'https://oss-cn-shenzhen.aliyuncs.com/',
    'ROLE_ARN': 'acs:ram::1709927201743129:role/aliyunosstokengeneratorrole',
    'TokenExpireTime': 60 * 60,
    'REGION': 'cn-shenzhen',
    'ROLE_SESSION_NAME': 'chisch',
    'BOUNDARY': '-'*10 + 'chisch' + '-'*10,
    'OBJECT_KEYS_SUB_ELEMENTS': {
        'upload_user_avatar': {
            'path': 'image/user/avatar/',
            'only_one': True,
        },
        'upload_dynamic': {
            'path': 'image/user/dynamic/',
            'only_one': False,
        },
        'upload_video_cover': {
            'path': 'image/user/avatar/',
            'file_suffix': '.mp4',
            'only_one': False,
        },
    }
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

