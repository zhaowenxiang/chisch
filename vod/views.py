# -*- coding: utf-8 -*-

import logging

from chisch.common.retwrapper import RetWrapper
import cores


logger = logging.getLogger('django')


def signature_url(request):
    params_query_dict = request.GET
    params = {k: v for k, v in params_query_dict.items()}
    try:
        url = cores.get_url()
    except Exception, e:
        return RetWrapper.wrap_and_return(e)
    result = {'url': url}
    return RetWrapper.wrap_and_return(result)
