from copy import deepcopy

from twisted.internet.defer import succeed
from twisted.trial.unittest import TestCase

from querryl.providers.search import SearchProvider


class FakeSearch(object):
    """
    A fake L{querryl.iquerryl.SearchProvider} for testing.
    """
    def getUser(self, username=None, userid=None):
        return succeed([(1, 'tester', 'hashedPassword')])



class Test_SearchProvider(TestCase):
    """
    Tests for L{querryl.providers.search.SearchProvider}.
    """
    def test_dictifyResults(self):
        """
        L{dictifyResults} takes a list results and returns a dictionary.
        """
        def checkDict(results, dictionary):
            for item in results:
                if item not in dictionary.values():
                    return False
            return True

        results = ('1', 'TestNetwork', '#test', '1245', 'tester', 'hello!')
        dictResult = SearchProvider().dictifyResults(deepcopy(results))
        self.assertTrue(checkDict(results, dictResult))


    def test_parseSender(self):
        """
        Parses a sender string and returns the nickname.
        """
        sender = 'tester!~test@my.host.mask'
        nickname = SearchProvider().parseSender(sender)
        self.assertEquals('tester', nickname)


    def test_processResults(self):
        """
        Turns results into a dictionary and replaces the sender with the
        nickname.
        """
        def checkResults(r):
            r[0]['sender'] += '!~test@host.mask'
            for item in results[0]:
                if item not in r[0].values():
                    return False
            return True

        results = [(
            '1', '123', '1', 'TestNetwork', '#test', '1245',
            'tester!~test@host.mask', 'hello!')]
        newResults = SearchProvider().processResults(deepcopy(results))

        self.assertEquals(newResults[0]['sender'], 'tester')
        self.assertTrue(checkResults(newResults))
