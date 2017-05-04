# -*- coding: utf-8 -*-

import os

from chisch.common.upload_file_analysis import parse_multipart_form_data


class UploadMiddleware(object):

    def process_request(self, request):
        if request.META['CONTENT_TYPE'] != 'multipart/form-data':
            pass
        else:
            arguments, files = parse_multipart_form_data(request._body)
            self.files = files
            body = {
                'action': None,
                'params': {
                    'files': []
                },
            }
            request._body = body
            for args in arguments:
                if args['name'] == 'action':
                    body['action'] = args['value']
                else:
                    body['params'][args['name']] = args['value']
            for f in files:
                body['params']['files'].append(f)

    def process_response(self, request, response):
        if hasattr(self, 'files'):
            for f in self.files:
                os.remove(f['path'])
        return response



