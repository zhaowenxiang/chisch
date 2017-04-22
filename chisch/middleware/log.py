# -*- coding: utf-8 -*-

import logging


logger = logging.getLogger('common')


class LogMiddleware(object):

    def process_request(self, request):
        full_path = request.get_full_path
        meta = request.META

        if request.method in ['POST', 'PUT']:
            body = request.body
            logger.info({'full_path': full_path, 'body': body,
                         'meta': meta})

        elif request.method in ['GET', 'DELETE']:
            logger.info({'full_path': full_path,
                         'meta': meta})
