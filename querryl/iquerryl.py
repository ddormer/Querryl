from zope.interface import Interface


class ISearchProvider(Interface):
    """
    A Quassel database searching service.
    """
    def getUsername(userid):
        """
        Returns the username matching the userid.

        @type userid: C{str}

        @rtype: C{unicode}
        """


    def getUserId(username):
        """
        Returns the userid matching the username.

        @type username: C{unicode}

        @rtype: C{str}
        """


    def getUser(username=None, userid=None):
        """
        Get a Quassel user's details.

        @type username: C{unicode}.
        @param username: The username of the user.
        """


    def search(query, username, startTime=None, endTime=None, channel=None):
        """
        Searches a Quassel database for the query. The search is limited to
        the user's buffers.

        @type query: C{unicode}
        @param query: The text to search for.

        @type username: C{unicode}
        @param username: The name of the user searching.

        @type time: C{tuple}
        @param time: The date start and end range to filter searches by.

        @type channel: C{unicode}
        @param channel: The channel to limit the search to.

        @rtype: C{dict}
        """


    def retrieveMessageBlock(bufferid, messageid, limit):
        """
        Retrieves a number of messages before and after the messageid.

        @type messageid: C{int}

        @type limit: C{int}
        """
