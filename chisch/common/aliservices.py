# -*- coding: utf-8 -*-

from mns.account import Account
from mns.topic import DirectSMSInfo
from mns.topic import TopicMessage

from django.conf import settings
from chisch.common.constents import (
    VERIFY_CODE_EFFECTIVE_TIME
)


class MnsService(object):

    def __init__(self):
        mns = settings.MNS
        access_key_id = mns.get('ACCESS_KEY_ID')
        access_key_secret = mns.get('ACCESS_KEY_SECRET')
        endpoint = mns.get('ENDPOINT')
        sign_name = mns.get('SIGN_NAME')
        template_code = mns.get('TEMPLATE_CODE')
        topic = mns.get('TOPIC')

        self.queue_name = mns.get('QUEUE_NAME')
        my_account = Account(endpoint, access_key_id, access_key_secret)
        self.my_account = my_account
        self.topic = my_account.get_topic(topic)
        self.message = "sms-message."
        self.direct_sms_attr = DirectSMSInfo(free_sign_name=sign_name,
                                             template_code=template_code,
                                             single=False)

    def publish_message(self, receiver, params):
        params['expiry'] = str(VERIFY_CODE_EFFECTIVE_TIME/60)
        self.direct_sms_attr.add_receiver(receiver=receiver,
                                          params=params)

        msg = TopicMessage(self.message, direct_sms=self.direct_sms_attr)
        re_msg = self.topic.publish_message(msg)
        return

