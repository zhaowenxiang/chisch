#! -*- coding: utf-8 -*-

import simplejson
from dss.Serializer import serializer


def s(data, own=True, extra=None):
    if extra is not None:
        for k, v in extra.items():
            data.__dict__[k] = v
    result = serializer(data,
                        own=own,
                        datetime_format='string',
                        output_type='json').replace("\n", "").replace(" ", "")
    return simplejson.loads(result)