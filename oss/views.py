# -*- coding: utf-8 -*-


from chisch.common import dependency
from chisch.common.retwrapper import RetWrapper
from chisch.common.serializer import s as _s
from chisch.common.views import DetailView


@dependency.requires('user_manager', 'oss_manager')
class OssDetail(DetailView):

    def get_sts_token(self, request):

        try:
            sts_token = self.oss_manager.create_sts_token(request)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)

        result = _s(sts_token)
        return RetWrapper.wrap_and_return(result)

