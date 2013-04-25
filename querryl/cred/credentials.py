from zope.interface import implements

from twisted.cred.credentials import IUsernameHashedPassword
from twisted.cred.error import UnauthorizedLogin, LoginFailed
from twisted.cred.checkers import ICredentialsChecker
from twisted.internet import defer

from querryl.cred.icred import ISessionCredentials


class SessionCredentials:
    implements(ISessionCredentials)

    def __init__(self, username):
        self.username = username


    def checkUsername(self):
        if self.username:
            return self.username



class SessionChecker(object):
    """
    A credential checker that handles a L{ISessionCredentials} credential and
    checks it against a session.
    """
    implements(ICredentialsChecker)
    credentialInterfaces = ISessionCredentials

    def requestAvatarId(self, credentials):
        avatar = credentials.checkUsername()
        if avatar:
            return defer.succeed(avatar)
        return defer.fail(UnauthorizedLogin())



class QuasselChecker(object):
    """
    A credential checker that handles a L{IUsernameHashedPassword} credential
    and checks it against a Quassel database.

    @ivar search: L{querryl.iquerryl.ISearchProvider}.
    """
    implements(ICredentialsChecker)
    credentialInterfaces = IUsernameHashedPassword

    def __init__(self, search):
        self.search = search

    def requestAvatarId(self, credentials):
        def cb(user):
            if user:
                if credentials.checkPassword(user[0][2]):
                    return defer.succeed(credentials.username)
            return defer.fail(UnauthorizedLogin())

        def eb(failure):
            return defer.fail(LoginFailed())

        d = self.search.getUser(username=credentials.username)
        d.addCallbacks(cb, eb)
        return d
