import sqlite3
from zope.interface import implements

from twisted.internet.defer import gatherResults
from twisted.enterprise import adbapi

from querryl.iquerryl import ISearchProvider
from querryl.error import SearchError
from querryl.providers.search import SearchProvider


class SqliteSearch(SearchProvider):
    implements(ISearchProvider)

    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.pool = adbapi.ConnectionPool("sqlite3", path)


    def getUsername(self, userid):
        return self.getUser(userid=userid).addCallback(
            lambda info: info[0][1])


    def getUserId(self, username):
        def _getUser(info):
            if len(info):
                if len(info[0]):
                    return info[0][0]
            return None
        return self.getUser(username=username).addCallback(_getUser)


    def getUser(self, username=None, userid=None):
        """
        Get a user's information.

        @param username: The username to of the user to retrieve data for.
        @type username: C{str}

        @param username: The userid to of the user to retrieve data for.
        @type username: C{int}
        """
        if username:
            d = self.pool.runQuery(
                u'SELECT * from quasseluser WHERE username == ?', (username,))
        if userid:
            d = self.pool.runQuery(
                u'SELECT * from quasseluser WHERE userid == ?', (userid,))
        return d


    def getBuffer(self, userid, channel):
        return self.pool.runQuery(
            u'SELECT * FROM buffer WHERE userid = ? AND buffername = ?',
            (userid, channel))


    def getBuffers(self, userid):
        return self.pool.runQuery(
            u'SELECT * FROM buffer WHERE userid = ?', (userid,))


    def _searchBuffer(self, buffer, text, startTime, endTime):
        """
        Search a single buffer.
        """
        query = '''
            SELECT backlog.bufferid, backlog.messageid, backlog.type,
            network.networkname, buffer.buffername,
            backlog.time, sender.sender, backlog.message
            FROM backlog
            JOIN sender ON backlog.senderid = sender.senderid
            JOIN buffer ON backlog.bufferid = buffer.bufferid
            JOIN network ON buffer.networkid = network.networkid
            WHERE backlog.message LIKE ? AND buffer.bufferid = ?
            AND backlog.type = 1 AND backlog.time BETWEEN ? AND ?'''
        args = ['%'+text+'%',
                buffer[0][0],
                startTime or 0,
                endTime or 9999999999999]
        return self.pool.runQuery(query, args)


    def _searchBuffers(self, buffers, text, startTime, endTime):
        """
        Search multiple buffers.
        """
        print "Warning: searching all buffers, this will probably take a very long time."
        args = [buff[0] for buff in buffers]
        query = '''
            SELECT backlog.bufferid, backlog.messageid,
            backlog.type, network.networkname, buffer.buffername,
            backlog.time, sender.sender, backlog.message
            FROM backlog
            JOIN sender ON backlog.senderid = sender.senderid
            JOIN buffer ON backlog.bufferid = buffer.bufferid
            JOIN network ON buffer.networkid = network.networkid
            WHERE backlog.message LIKE ?
            AND buffer.bufferid IN (%s)
            AND backlog.type = 1''' % (','.join(['?'] * len(args)))
        args.insert(0, '%'+text+'%')
        return self.pool.runQuery(query, args)


    def retrieveMessageBlock(self, userid, bufferid, messageid, limit):
        """
        Retrieves a number of messages before and after the messageid.

        @type messageid: C{int}

        @type limit: C{int}
        """
        def checkUser(buffers):
            for buffer in buffers:
                if int(bufferid) == buffer[0]:
                    return bufferid
            raise SearchError("User doesn't have access to buffer")

        def _combine(results):
            return results[0] + results[1]

        def getMessages(bufferid):
            ds = [
                self._retrievePreviousMessages(bufferid, messageid, limit),
                self._retrieveFutureMessages(bufferid, messageid, limit)]
            d2 = gatherResults(ds, consumeErrors=True)
            d2.addCallback(_combine)
            d2.addCallback(self.processResults)
            return d2

        d1 = self.getBuffers(userid)
        d1.addCallback(checkUser)
        d1.addCallback(getMessages)
        return d1


    def _retrievePreviousMessages(self, bufferid, messageid, limit):
        def _reverse(results):
            results.reverse()
            return results

        q = '''
            SELECT backlog.bufferid, backlog.messageid,
            backlog.type, network.networkname, buffer.buffername,
            backlog.time, sender.sender, backlog.message
            FROM backlog
            JOIN sender ON backlog.senderid = sender.senderid
            JOIN buffer ON backlog.bufferid = buffer.bufferid
            JOIN network ON buffer.networkid = network.networkid
            WHERE buffer.bufferid = ?
            AND backlog.type = 1
            AND backlog.messageid <= ? ORDER BY backlog.messageid DESC LIMIT ?'''
        d = self.pool.runQuery(q, [bufferid, messageid, limit])
        d.addCallback(_reverse)
        return d


    def _retrieveFutureMessages(self, bufferid, messageid, limit):
        q = '''
            SELECT backlog.bufferid, backlog.messageid,
            backlog.type, network.networkname, buffer.buffername,
            backlog.time, sender.sender, backlog.message
            FROM backlog
            JOIN sender ON backlog.senderid = sender.senderid
            JOIN buffer ON backlog.bufferid = buffer.bufferid
            JOIN network ON buffer.networkid = network.networkid
            WHERE buffer.bufferid = ?
            AND backlog.type = 1
            AND backlog.messageid > ? LIMIT ?'''
        return self.pool.runQuery(q, [bufferid, messageid, limit])


    def search(self, query, username, startTime=None, endTime=None, channel=None):
        if not query:
            raise SearchError("No query specified.")
        if not username:
            raise SearchError("No username specified.")

        def checkBuffers(buffers, channel=None):
            if buffers:
                return buffers
            if channel:
                raise SearchError("Channel %s does not exist." % (channel,), 404)
            raise SearchError("User has no buffers.")

        d = self.getUserId(username)
        if channel:
            d.addCallback(self.getBuffer, channel)
            d.addCallback(checkBuffers, channel)
            d.addCallback(self._searchBuffer, query, startTime, endTime)
        else:
            d.addCallback(self.getBuffers)
            d.addCallback(checkBuffers)
            d.addCallback(self._searchBuffers, query, startTime, endTime)
        d.addCallback(self.processResults)
        return d
