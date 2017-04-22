#! -*- coding: utf-8 -*-

import simplejson
from django.db import models
from dss.Serializer import serializer
from django.db.models.query import QuerySet


def to_json(obj, **kwargs):

    exclude_attr = kwargs['exclude_attr'] if kwargs and 'exclude_attr' in kwargs  else []
    include_attr = kwargs['include_attr'] if kwargs and 'include_attr' in kwargs  else []

    return serializer(
        obj,
        datetime_format='string',
        output_type='json',
        exclude_attr=exclude_attr,
        include_attr=include_attr)
