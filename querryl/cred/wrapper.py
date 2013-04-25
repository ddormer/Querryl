import cgi
import hashlib

from twisted.cred import error
from twisted.cred.credentials import Anonymous
from twisted.cred.credentials import UsernameHashedPassword, IAnonymous
from twisted.web.resource import IResource, ErrorPage
from twisted.web.guard import HTTPAuthSessionWrapper
from twisted.web import util
from twisted.python import log

from querryl.cred.user import IUserStorage
from querryl.cred.credentials import SessionCredentials
from querryl.resources import _UnauthorizedResource


class BasicWrapper(HTTPAuthSessionWrapper):
    """
    Wraps a L{twisted.cred.portal.Portal} to support form and session
    authentication.
    """
    def _authorizedResource(self, request):
        session = request.getSession()
        self.headers = request.getAllHeaders()

        # Does the user have an authorized session?
        if IUserStorage(session).name:
            userStorage = IUserStorage(session)
            credentials = SessionCredentials(userStorage.name)
            return util.DeferredResource(self._login(credentials, request))

        # Check if the request is an HTTP authentication form.
        elif 'content-type' in self.headers and (
            self.headers['content-type'] == 'application/x-www-form-urlencoded'):

            form = cgi.FieldStorage(
                fp = request.content,
                headers = self.headers,
                environ = {
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['content-type']})

            # Is the form valid?
            try:
                form['login']
                username = request.args['username'][0]
                password = request.args['password'][0]
            except KeyError:
                return util.DeferredResource(self._login(Anonymous(), request))

            credentials = UsernameHashedPassword(unicode(username),
                    unicode(hashlib.new('sha1', password).hexdigest()))
            return util.DeferredResource(self._login(credentials, request))
        return util.DeferredResource(self._login(Anonymous(), request))


    def _login(self, credentials, request):
        def _setSession(d):
            session = IUserStorage(request.getSession())
            session.name = credentials.username
            return d

        d = self._portal.login(credentials, None, IResource)
        if not IAnonymous in credentials.__implemented__:
            d.addCallback(_setSession)
        d.addCallbacks(self._loginSucceeded, self._loginFailed)
        return d


    def _loginFailed(self, result):
        """
        Handle login failure by presenting either another challenge (for
        expected authentication/authorization-related failures) or a server
        error page (for anything else).
        """
        if result.check(error.Unauthorized, error.LoginFailed):
            return _UnauthorizedResource(self._credentialFactories)
        else:
            log.err(
                result,
                "HTTPAuthSessionWrapper.getChildWithDefault encountered "
                "unexpected error")
            return ErrorPage(500, None, None)
