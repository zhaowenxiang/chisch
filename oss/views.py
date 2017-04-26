# -*- coding: utf-8 -*-


from chisch.common import dependency
from chisch.common.retwrapper import RetWrapper
from chisch.common.serializer import s as _s
from chisch.common.views import DetailView


@dependency.requires('user_manager', 'oss_manager')
class OssDetail(DetailView):

    def get_sts_token(self, request, *args, **kwargs):

        purpose = kwargs['purpose']
        attached_object_id = kwargs['attached_object_id']

        try:
            sts_token = self.oss_manager.get_sts_token(purpose,
                                                       attached_object_id)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)

        result = _s(sts_token)
        return RetWrapper.wrap_and_return(result)

