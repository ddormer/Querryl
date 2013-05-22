import json

from twisted.web._auth.wrapper import UnauthorizedResource
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.template import Element, XMLFile, flattenString
from twisted.python.filepath import FilePath
from twisted.python.failure import Failure

from querryl.utils import FailureEncoder


class LoginElement(Element):
    loader = XMLFile(FilePath('querryl/templates/login.html'))



class SearchElement(Element):
    loader = XMLFile(FilePath('querryl/templates/search.html'))



class _UnauthorizedResource(UnauthorizedResource):
    """
    Simple IResource to escape Resource dispatch
    """
    def render(self, request):
        request.setResponseCode(401)
        return 'Unauthorized'



class LoginPage(Resource):
    """
    The login page.
    """
    def __init__(self, avatarId):
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



class BaseResource(Resource):
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
            request.setResponseCode(500)
            if hasattr(d.value, 'errorCode'):
                if d.value.errorCode:
                    request.setResponseCode(d.value.errorCode)
            request.write(json.dumps(d, cls=FailureEncoder))
        else:
            request.write(json.dumps(d))
        request.finish()


    def extractArgs(self, request, arguments):
        args = []
        for argument in arguments:
            arg = request.args.get(argument)
            if not arg:
                args.append(None)
            else:
                args.append(arg[0])
        return args



class Search(BaseResource):
    """
    RESTful resource for using L{querryl.iquerryl.search}.
    """
    def render_GET(self, request):
        accept = request.getHeader('Accept')

        arguments = self.extractArgs(request, ('query', 'startTime', 'endTime', 'channel'))
        arguments.insert(1, self.avatarId)

        if 'application/json' in accept:
            d = self.search.search(*arguments)
            d.addBoth(self.write_JSON, request)
            return NOT_DONE_YET

        if 'text/html' in accept:
            return "Put some parameter information here."

        return "Unsupported 'Accept' header"



from querryl.cred.user import IUserStorage
class GetBlock(BaseResource):
    """
    RESTful resource for using L{querryl.iquerryl.retrieveMessageBlock}.
    """
    def getBlock(self, request, avatar):
        arguments = self.extractArgs(request, ('bufferid', 'messageid', 'backlogLimit'))
        arguments.insert(0, self.avatar.userid)

        d = self.search.retrieveMessageBlock(*arguments)
        d.addBoth(self.write_JSON, request)
        return d


    def render_GET(self, request):
        accept = request.getHeader('Accept')
        self.avatar = avatar = IUserStorage(request.getSession())

        def cb(userid, avatar):
            avatar.userid = userid
            return request

        if 'application/json' in accept:
            pass
        d = self.search.getUserId(self.avatarId)
        d.addCallback(cb, avatar)
        d.addCallback(self.getBlock, avatar)
        return NOT_DONE_YET

        return "Unsupported 'Accept' header"



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
