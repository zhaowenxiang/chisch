# -*- coding: utf-8 -*-

import uuid

from django.conf import settings


def parse_multipart_form_data(body=""):
    """Parses a ``multipart/form-data`` body.

    The ``boundary`` and ``body`` parameters are both byte strings.
    The dictionaries given in the arguments and files parameters
    will be updated with the contents of the body.
    """
    # The standard allows for the boundary to be quoted in the header,
    # although it's rare (it happens at least for google app engine
    # xmpp).  I think we're also supposed to handle backslash-escapes
    # here but I'll save that until we see a client that uses them
    # in the wild.
    boundary_eoh = body.find("\r\n")
    boundary = body[:boundary_eoh]

    arguments = []
    files = []

    if boundary.startswith(b'"') and boundary.endswith(b'"'):
        boundary = boundary[1:-1]
    final_boundary_index = body.rfind(boundary + b"--")
    if final_boundary_index == -1:
        return
    parts = body[:final_boundary_index].split(
        boundary + b"\r\n")
    for part in parts:
        if not part:
            continue
        eoh = part.find(b"\r\n\r\n")
        if eoh == -1:
            continue
        content_disposition = part[:part.find(b"\r\n")]
        disposition, disp_params = \
            _parse_content_disposition(content_disposition)
        if disposition != "Content-Disposition: form-data" or \
                not part.endswith(b"\r\n"):
            continue
        value = part[eoh + 4:-2]
        if not disp_params.get("name"):
            continue
        name = disp_params["name"]
        if disp_params.get("filename"):
            file_path = settings.OBJECT_LOCAL_TRANSFER_DIR + str(uuid.uuid1())
            with open(file_path, 'wb') as f:
                f.write(value)
            # file_type = _parse_file_type(part)
            f = {
                'name': name,
                'name': disp_params.get("filename"),
                # 'type': file_type,
                'path': file_path,
            }
            files.append(f)
        else:
            argument = {
                'name': name,
                'value': value,
            }
            arguments.append(argument)

    return arguments, files


def _parseparam(s):
    while s[:1] == ';':
        s = s[1:]
        end = s.find(';')
        while end > 0 and (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
            end = s.find(';', end + 1)
        if end < 0:
            end = len(s)
        f = s[:end]
        yield f.strip()
        s = s[end:]


def _parse_content_disposition(line):
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    """
    parts = _parseparam(';' + line)
    key = next(parts)
    pdict = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1:].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value
        else:
            pdict[p] = None
    return key, pdict


# def _parse_file_type(line):
#     ctype_list = []
#     ctype_eoh = line.find('Content-Type')
#     point = ctype_eoh + len('Content-Type') + 1
#     while True:
#         if line[point] in [None, ' ', ':']:
#             point += 1
#             continue
#         elif line[point] == '\r':
#             break
#         else:
#             ctype_list.append(line[point])
#             point += 1
#             continue
#     file_type = ''.join(ctype_list)
#     return '.' + file_type.split('/')[1]
