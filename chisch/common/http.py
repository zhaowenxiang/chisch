import urllib
import httplib


# def do_post(url, body, **header):
#     request = make_request(url, 'POST', body, **header)
#     try:
#         response = urllib2.urlopen(request)
#     except Exception, e:
#         raise e
#     return response


def do_get(url, **params):
    query = urllib.urlencode(params)
    _, rest = urllib.splittype(url)
    host, _ = urllib.splithost(rest)
    url += ('?' + query)
    try:
        conn = httplib.HTTPConnection(host)
        conn.request(method="GET", url=url)
    except Exception, e:
        raise e
    response = conn.getresponse()
    return response
