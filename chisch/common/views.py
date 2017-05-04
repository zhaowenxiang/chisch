# -*- coding: utf-8 -*-

import simplejson

from django.views import generic


class BaseView(object):

    def __init__(self, *args, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            if request.method in ['POST', 'PUT']:
                if isinstance(request.body, dict):
                    data = request.body
                else:
                    data = simplejson.loads(request.body)
                action = data.pop('action')
                kwargs.update(data.get('params', {}))
                handler = getattr(self, action, self.http_method_not_allowed)
            elif request.method == 'GET':
                action = request.GET.get('action', request.method.lower())
                handler = getattr(self, action, self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class DetailView(BaseView, generic.DetailView):
    def __init__(self, *args, **kwargs):
        super(DetailView, self).__init__(*args, **kwargs)


class ListView(BaseView, generic.DetailView):
    def __init__(self, *args, **kwargs):
        super(ListView, self).__init__(*args, **kwargs)
