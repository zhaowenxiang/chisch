# -*- coding: utf-8 -*-

import cgi
import logging
import struct

import tornado.httputil

from gp.fileupload import Storage
from gp.fileupload import purge_files

from django.db import transaction

from chisch.common.retwrapper import RetWrapper
from chisch.common import dependency
from chisch.common.decorators import login_required
from chisch.common.views import ListView, DetailView
from chisch.common.serializer import s as _s
from chisch.common.constents import (
    VERIFY_TYPE_CHANGE_PASSWORD as VTCP,
)


logger = logging.getLogger('django')


@dependency.requires('user_manager', 'verify_manager', 'auth_manager')
class UserDetailView(DetailView):

    @login_required
    def get(self, request, *args, **kwargs):
        # TODO
        user = self.user_manager.get(id=request.user.id)
        result = _s(user, **user.serializer_rule())
        return RetWrapper.wrap_and_return(result)

    @transaction.atomic
    def change_password(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user_name = args[0]
        new_password = kwargs.get('new_password', None)
        old_password = kwargs.get('old_password', None)
        verify_code = kwargs.get('verify_code', None)
        agent_idfa = kwargs.get('agent_idfa', None)

        try:
            user = self.user_manager.auth(user_name,
                                          password=old_password,
                                          verify_type=VTCP,
                                          verify_code=verify_code)
        except Exception, e:
            return RetWrapper.wrap_and_return(e)

        user.set_password(new_password)
        user.save()
        self.auth_manager.login(request,
                                user,
                                agent_idfa=agent_idfa,
                                flush_all_token=True)
        result = _s(user, **user.serializer_rule())
        return RetWrapper.wrap_and_return(result)

    @login_required
    @transaction.atomic
    def update(self, request, *args, **kwargs):

        user = self.user_manager.update(request.user, **kwargs)
        result = _s(user, **user.serializer_rule())
        return RetWrapper.wrap_and_return(result)

    @transaction.atomic
    def upload_avatar(self, request, *args, **kwargs):
        args = {}
        files = {}
        d = request.body
        separator = d[6:40]
        parse_multipart_form_data(separator, d, args, files)
        print args, files

def parse_multipart_form_data(boundary, data, arguments, files):
    """Parses a ``multipart/form-data`` body.

    The ``boundary`` and ``data`` parameters are both byte strings.
    The dictionaries given in the arguments and files parameters
    will be updated with the contents of the body.
    """
    # The standard allows for the boundary to be quoted in the header,
    # although it's rare (it happens at least for google app engine
    # xmpp).  I think we're also supposed to handle backslash-escapes
    # here but I'll save that until we see a client that uses them
    # in the wild.
    if boundary.startswith(b'"') and boundary.endswith(b'"'):
        boundary = boundary[1:-1]
    final_boundary_index = data.rfind(b"--" + boundary + b"--")
    if final_boundary_index == -1:
        gen_log.warning(
            "Invalid multipart/form-data: no final boundary")
        return
    parts = data[:final_boundary_index].split(
        b"--" + boundary + b"\r\n")
    for part in parts:
        if not part:
            continue
        eoh = part.find(b"\r\n\r\n")
        if eoh == -1:
            # gen_log.warning("multipart/form-data missing headers")
            continue
        headers = HTTPHeaders.parse(part[:eoh].decode("utf-8"))
        disp_header = headers.get("Content-Disposition", "")
        disposition, disp_params = _parse_header(disp_header)
        if disposition != "form-data" or not part.endswith(b"\r\n"):
            # gen_log.warning("Invalid multipart/form-data")
            continue
        value = part[eoh + 4:-2]
        if not disp_params.get("name"):
            # gen_log.warning("multipart/form-data value missing name")
            continue
        name = disp_params["name"]
        if disp_params.get("filename"):
            ctype = headers.get("Content-Type", "application/unknown")
            files.setdefault(name, []).append(HTTPFile(  # type: ignore
                filename=disp_params["filename"], body=value,
                content_type=ctype))
        else:
            arguments.setdefault(name, []).append(value)

        # a, = struct.unpack('i', request.body)
        # b = 10
        #
        # fields = cgi.FieldStorage(fp=request.environ['wsgi.input'],
        #                           environ=request.environ,
        #                           keep_blank_values=1)
        # image_str = kwargs['image']
        # import base64
        # with open('/root/a.png', 'wb') as fout:
        #     fout.write(base64.b64decode(image_str))
        # try:
        #     user = self.user_manager.upload_avatar()
        # except Exception, e:
        #     return RetWrapper.wrap_and_return(e)
        # return RetWrapper.wrap_and_return(user)


@dependency.requires('user_manager', 'verification_manager')
class UserListView(ListView):
    pass


