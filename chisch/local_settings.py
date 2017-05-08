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
    'VIDEO_SIGN_URL_EXPIRES': 60 * 60,   # 视频私有链接有效时间60分
    'REGION': 'cn-shenzhen',
    'ROLE_SESSION_NAME': 'chisch',
    'BOUNDARY': '-'*10 + 'chisch' + '-'*10,
    'OBJECT_KEYS_SUB_ELEMENTS': {
        'upload_user_avatar': {
            'path': 'image/user/avatar/',
            'only_one': True,
        },
        'create_curriculum': {
            'path': 'image/curriculum/cover/',
            'only_one': True,
        },
        'upload_video': {
            'path': 'video/',
            'file_suffix': '.mp4',
            'only_one': True,
        },
    }
}

# SMALL_OBJECT_UPPER_LIMIT = 1024 * 1024 * 10       # 小文件的定义规则为大小不超过10M
OBJECT_LOCAL_TRANSFER_DIR = '/tmp/chisch/transfer/'   # 本地转存路径
OBJECT_PREFERRED_SIZE = 1024 * 1024 * 2       # 分片大小,2M

IMAGE_TYPE = '.png'
VIDEO_TYPE = '.mp4'

MNS = {
    'ACCESS_KEY_ID': 'LTAIFSaBApB2TuC4',
    'ACCESS_KEY_SECRET': '0qMu5s3yHEBrxb2klSyZKnHmOPb0HZ',
    'ENDPOINT': 'https://1709927201743129.mns.cn-hangzhou.aliyuncs.com/',
    'SIGN_NAME': '千寻教育',
    'TEMPLATE_CODE': 'SMS_62440527',
    'TOPIC': 'sms.topic-cn-hangzhou',
    'QUEUE_NAME': 'verify-code-queue',
}


