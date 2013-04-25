import json

from twisted.web._auth.wrapper import UnauthorizedResource
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.template import Element, XMLFile, flattenString
from twisted.python.filepath import FilePath
from twisted.python.failure import Failure

from querryl.utils import FailureEncoder


class _UnauthorizedResource(UnauthorizedResource):
    """
    Simple IResource to escape Resource dispatch
    """
    def render(self, request):
        request.setResponseCode(401)
        return 'Unauthorized'



class LoginElement(Element):
    loader = XMLFile(FilePath('templates/login.html'))



class LoginPage(Resource):
    """
    The login page.
    """
    def __init__(self, avatarId, search):
        self.avatar = avatarId


    def render_POST(self, request):
        request.redirect('/')
        request.finish()
        return NOT_DONE_YET


    def render_GET(self, request):
        def _renderDone(html):
            request.write(html)
            request.finish()

        if self.avatar:
            request.redirect('/')

        flattenString(None, LoginElement()).addCallback(_renderDone)
        return NOT_DONE_YET



class Search(Resource):
    """
    RESTful resource for using L{querryl.iquerryl.search}.
    """
    def __init__(self, avatarId, search):
        self.avatarId = avatarId
        self.search = search


    def write_JSON(self, d, request):
        """
        Turns either a Failure or a set of results into JSON then writes it to
        C{request}.

        @type d: L{Failure} or C{list}
        @param d: The failure produced by the search provider or the results.
        """
        request.setHeader('content-type', 'application/json')

        if isinstance(d, Failure):
            request.write(json.dumps(d, cls=FailureEncoder))
        else:
            request.write(json.dumps(d))
        request.finish()


    def render_GET(self, request):
        accept = request.getHeader('Accept')
        args = request.args

        if 'application/json' in accept:
            d = self.search.search(
                    args.get('query', [None])[0],
                    self.avatarId,
                    args.get('startTime', [None])[0],
                    args.get('endTime', [None])[0],
                    args.get('channel', [None])[0])
            d.addBoth(self.write_JSON, request)
            return NOT_DONE_YET
        if 'text/html' in accept:
            return "Put some parameter information here."

        return "Unsupported 'Accept' header"



class GetBlock(Search):
    """
    RESTful resource for using L{querryl.iquerryl.retrieveMessageBlock}.
    """
    def render_GET(self, request):
        return None



class SearchElement(Element):
    loader = XMLFile(FilePath('templates/search.html'))



class SearchRoot(Resource):
    """
    The search page. This is the first page a user will see after logging in.
    """
    def __init__(self, avatarId, search):
        self.avatarId = avatarId
        self.search = search


    def render_GET(self, request):
        def _renderDone(html):
            request.write(html)
            request.finish()

        flattenString(None, SearchElement()).addCallback(_renderDone)
        return NOT_DONE_YET
