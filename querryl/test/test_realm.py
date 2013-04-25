from twisted.trial.unittest import TestCase
from twisted.web.resource import IResource

from querryl.cred.realm import PublicHTMLRealm


class PublicHTMLRealmTests(TestCase):
    """
    Tests for L{querryl.cred.realm.PublicHTMLRealm}.
    """
    def setUp(self):
        self.realm = PublicHTMLRealm(None)


    def test_requestAvatarAnonymous(self):
        """
        L{PublicHTMLRealm.requestAvatar} returns a
        L{twisted.web.resource.Resource} if C{avatarId} is C{None}.
        """
        self.assertTrue(
            IResource in self.realm.requestAvatar(None, None, IResource))


    def test_requestAvatarRegistered(self):
        """
        L{PublicHTMLRealm.requestAvatar} returns a
        L{twisted.web.resource.Resource} if C{avatarId} is not L{None
        """
        self.assertTrue(
            IResource in self.realm.requestAvatar('username', None, IResource))


    def test_requestAvatarNoInterface(self):
        """
        L{PublicHTMLRealm.requestAvatar} raises a L{NotImplementedError} if
        the interface argument does not contain an L{IResource}.
        """
        self.assertRaises(
            NotImplementedError,
            self.realm.requestAvatar, 'username', None, [])
