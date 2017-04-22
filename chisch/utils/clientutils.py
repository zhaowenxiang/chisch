class ClientInfoGenerator(object):

    __instance = None

    def __init__(self):
        pass

    @classmethod
    def get_client_ip(cls, request):
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        return ip
