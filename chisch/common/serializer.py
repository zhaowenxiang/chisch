#! -*- coding: utf-8 -*-

import simplejson
from dss.Serializer import serializer


def s(data, **kwargs):
    extra_attr = kwargs.get('extra_attr', {})
    for extra in extra_attr:
        data.__dict__[extra] = getattr(data, extra, None)
    include_attr = kwargs.get('include_attr', None)
    exclude_attr = kwargs.get('exclude_attr', None)
    foreign = kwargs.get('foreign', True)
    many = kwargs.get('many', False)
    through = kwargs.get('through', True)

    result = serializer(data,
                        datetime_format='string',
                        output_type='json',
                        include_attr=include_attr,
                        exclude_attr=exclude_attr,
                        foreign=foreign,
                        many=many,
                        through=through).replace("\n", "").replace(" ", "")
    return simplejson.loads(result)