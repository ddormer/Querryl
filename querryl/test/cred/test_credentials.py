"""
Tests for L{querryl.cred.credentials}.
"""
from twisted.trial.unittest import TestCase
from twisted.cred.error import UnauthorizedLogin
from twisted.cred.credentials import UsernameHashedPassword

from querryl.cred.icred import ISessionCredentials
from querryl.cred.credentials import (
    SessionCredentials, SessionChecker, QuasselChecker)
from querryl.test.providers.test_search import FakeSearch


class Test_SessionCredentials(TestCase):
    """
    Tests for L{querryl.cred.credentials.SessionCredentials}.
    """
    def test_checkUsername(self):
        """
        L{checkUsername} returns C{self.username}.
        """
        username = 'tester'
        session = SessionCredentials(username)
        self.assertEquals(username, session.checkUsername())



class Test_SessionChecker(TestCase):
    """
    Tests for L{querryl.cred.credentials.SessionChecker}.
    """
    def test_requestAvatarIdImplements(self):
        """
        L{requestAvatarId} supports L{ISessionCredentials}.
        """
        checker = SessionChecker()
        self.assertEquals(checker.credentialInterfaces, ISessionCredentials)


    def test_requestAvatarId(self):
        """
        L{requestAvatarId} returns an avatar if the credentials are valid.
        """
        checker = SessionChecker()
        def cb(d):
            self.assertEquals('tester', d)

        d = checker.requestAvatarId(SessionCredentials('tester'))
        d.addCallback(cb)
        return d


    def test_requastAvatarIdIncorrect(self):
        """
        L{requestAvatarId} returns a L{Failure} containing a
        L{UnauthorizedLogin} if the credentials are incorrect.
        """
        checker = SessionChecker()
        credentials = SessionCredentials('')
        return self.assertFailure(
            checker.requestAvatarId(credentials),
            UnauthorizedLogin)



class Test_QuasselChecker(TestCase):
    """
    Tests for L{querryl.cred.credentials.QuasselChecker}.
    """
    def test_requestAvatarId(self):
        """
        L{requestAvatarId} returns an avatar if the credentials are valid.
        """
        def cb(avatar):
            self.assertEquals('tester', avatar)

        credentials = UsernameHashedPassword('tester', 'hashedPassword')
        checker = QuasselChecker(FakeSearch())

        d = checker.requestAvatarId(credentials)
        d.addCallback(cb)
        return d


    def test_requestAvatarIdIncorrect(self):
        """
        L{requestAvatarId} returns L{UnauthorizedLogin} if the credentials are
        incorrect.
        """
        checker = QuasselChecker(FakeSearch())
        credentials = UsernameHashedPassword('tester', 'wrongHash')
        return self.assertFailure(
            checker.requestAvatarId(credentials),
            UnauthorizedLogin)
