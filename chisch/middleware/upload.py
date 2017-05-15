# -*- coding: utf-8 -*-

import os

from chisch.common.upload_file_analysis import parse_multipart_form_data


class UploadMiddleware(object):

    def process_request(self, request):

        request.upload_files_path = []
        if 'multipart/form-data' not in request.META['CONTENT_TYPE']:
            pass
        else:
            data = request.body
            arguments, files = parse_multipart_form_data(data)
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
                request.upload_files_path.append(f['path'])

    def process_response(self, request, response):
        if hasattr(request, 'upload_file_ids') and \
                        len(request.upload_file_ids) > 0:
            for path in self.request.upload_files_path:
                os.remove(path)
        return response
