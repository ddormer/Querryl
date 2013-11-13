import json

from twisted.python.failure import Failure
from twisted.web.util import Redirect


class FailureEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Failure):
            return {'error': obj.value.message}



class RedirectFromRequest(Redirect):
    def __init__(self, port):
        self.port = port
        Redirect.__init__(self, None)


    def render(self, request):
        self.url = 'https://%s:%s' % (
            request.getRequestHostname(),
            self.port)
        return Redirect.render(self, request)
