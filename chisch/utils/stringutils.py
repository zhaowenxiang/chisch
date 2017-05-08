# -*- coding: utf-8 -*-

import random
import uuid

from chisch.common.constents import VERIFY_CODE_LENGTH


def generate_verify_code():
    min_code = pow(10, VERIFY_CODE_LENGTH - 1)
    max_code = pow(10, VERIFY_CODE_LENGTH) - 1
    code_range = random.randint(min_code, max_code)
    return str(code_range)


def generate_token():
    return str(uuid.uuid4())

