from querryl.error import SearchError


class SearchProvider(object):
    """
    A base class for L{querryl.iquerryl.ISearchProvider}.
    """
    def dictifyResults(self, results):
        """
        Turns the result tuple into a more usable dictionary.

        @type results: C{tuple}
        @param results: A single search result.

        @rtype: C{dict}
        """
        keys = ['bufferid', 'messageid', 'bType', 'networkName', 'bufferName', 'time', 'sender', 'message']
        return dict(zip(keys, results))


    def parseSender(self, sender):
        """
        Retrieves the nickname from a hostmask.

        @type sender: C{unicode} or C{str}
        @param sender: The sender's hostmask.

        @rtype: C{unicode} or C{str}
        @return: A nickname.
        """
        return sender.split('!')[0]


    def processResults(self, results):
        """
        Does any processing required on the search results.

        @type results: C{list}
        @param results: A list containing a tuple of search results.

        @rtype: C{list} containing C{dict}
        """
        processed = []
        if results:
            for res in results:
                res = list(res)
                res[6] = self.parseSender(res[6])
                processed.append(self.dictifyResults(res))
        else:
            raise SearchError('No results were found.', 404)
        return processed
