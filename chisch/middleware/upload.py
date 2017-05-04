# -*- coding: utf-8 -*-

import os

from chisch.common.upload_file_analysis import parse_multipart_form_data


class UploadMiddleware(object):

    def process_request(self, request):
        if request.content_type != 'multipart/form-data':
            pass
        else:
            arguments, files = parse_multipart_form_data(request._body)
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
        for f in request.body['params']['files']:
            os.remove(f['path'])
        return response



