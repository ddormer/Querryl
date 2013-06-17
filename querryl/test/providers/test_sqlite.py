from twisted.python.filepath import FilePath
from twisted.trial.unittest import TestCase

from querryl.providers.sqlite import SqliteSearch


class Test_SqliteSearch(TestCase):
    """
    Tests for L{querryl.providers.sqlite.SqliteSearch}.
    """
    def setUp(self):
        path = FilePath(__file__).sibling('data').child('quassel-storage.sqlite')
        self.ss = SqliteSearch(path.path)


    def test_getUsername(self):
        """
        L{getUsername} takes a userid and returns the username belonging to
        the userid.
        """
        def cb(username):
            self.assertEquals(username, 'tester')

        d = self.ss.getUsername('1')
        d.addCallback(cb)
        return d


    def test_getUserId(self):
        """
        L{getUserId} takes a username argument and returns the userid belonging
        to the username.
        """
        def cb(userid):
            self.assertEquals(userid, 1)

        d = self.ss.getUserId('tester')
        d.addCallback(cb)
        return d


    def test_getUserUsername(self):
        """
        L{getUser} takes a username kwarg and returns the user's information.
        """
        def cb(userid):
            self.assertEquals(userid, [(1, u'tester', u'password')])

        d = self.ss.getUser(username='tester')
        d.addCallback(cb)
        return d


    def test_getUserUserid(self):
        """
        L{getUser} takes a userid kwarg and returns the user's information.
        """
        def cb(username):
            self.assertEquals(username, [(1, u'tester', u'password')])

        d = self.ss.getUser(userid=1)
        d.addCallback(cb)
        return d


    def test_getUserNoUser(self):
        """
        L{getUser} will return an empty list if the user doesn't exist.
        """
        def cb(username):
            self.assertEquals(username, [])

        d = self.ss.getUser(username='1')
        d.addCallback(cb)
        return d


    def test_getBuffer(self):
        """
        L{getBuffer} takes a userid, channel and network then returns a buffer.
        """
        def cb(d):
            self.assertEquals(
                d, [(1, 1, None, 1, u'#test', u'#test', 2, 71, 0, None, 1)])

        d = self.ss.getBuffer(1, '#test', networkid=1)
        d.addCallback(cb)
        return d


    def test_getBuffers(self):
        """
        L{getBuffers} takes a userid and returns a list of buffers.
        """
        def cb(d):
            self.assertEquals(
                d, [
                    (1, 1, None, 1, u'#test', u'#test', 2, 71, 0, None, 1),
                    (3, 1, 1, 2, u'#test3', u'#test3', 1, 1, 1, u'1', 1)])

        d = self.ss.getBuffers(1)
        d.addCallback(cb)
        return d


    def test_getBuffersNetwork(self):
        """
        L{getBuffers} takes a kwarg named 'networkid' that limits the search to
        one network.
        """
        def cb(d):
            self.assertEquals(
                d, [(3, 1, 1, 2, u'#test3', u'#test3', 1, 1, 1, u'1', 1)])

        d = self.ss.getBuffers(1, networkid=2)
        d.addCallback(cb)
        return d
