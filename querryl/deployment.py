from twisted.application import service, internet
from twisted.internet.ssl import DefaultOpenSSLContextFactory

from twisted.cred.checkers import AllowAnonymousAccess
from twisted.cred.credentials import IUsernameHashedPassword
from twisted.cred.portal import Portal
from twisted.web import server

from querryl.cred.credentials import (
    ISessionCredentials, SessionChecker, QuasselChecker)
from querryl.cred.realm import PublicHTMLRealm
from querryl.cred.wrapper import BasicWrapper
from querryl.providers.sqlite import SqliteSearch


searchServices = {
    'sqlite': SqliteSearch
    }


def deploy(iface, port, dbPath, dbType, ssl=False, sslPrivate=None, sslCert=None, sslPort=None):
    searchService = searchServices[dbType](dbPath)

    portal = Portal(PublicHTMLRealm(searchService), [AllowAnonymousAccess()])
    portal.registerChecker(QuasselChecker(searchService), IUsernameHashedPassword)
    portal.registerChecker(SessionChecker(), ISessionCredentials)

    application = service.Application("Querryl")
    site = server.Site(BasicWrapper(portal, []))

    if ssl:
        ctx = DefaultOpenSSLContextFactory(sslPrivate, sslCert)
        ssl_sv = internet.SSLServer(sslPort, site, ctx, interface=iface)
        ssl_sv.setServiceParent(application)

    sv = internet.TCPServer(port, site, interface=iface)
    sv.setServiceParent(application)
    return application
