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
from querryl.providers.postgresql import PostgresqlSearch
from querryl.utils import RedirectFromRequest


searchServices = {
    'sqlite': SqliteSearch,
    'postgresql': PostgresqlSearch}


class LongSession(server.Session):
    sessionTimeout = 172800



def deploy(iface, port, dbLocation, dbType, dbUsername=None, dbPassword=None,
           ssl=False, sslRedirect=False, sslPrivate=None, sslCert=None,
           sslPort=None):

    if dbUsername and dbPassword:
        searchService = searchServices[dbType](
            dbLocation, dbUsername, dbPassword)
    else:
        searchService = searchServices[dbType](dbLocation)

    portal = Portal(PublicHTMLRealm(searchService), [AllowAnonymousAccess()])
    portal.registerChecker(QuasselChecker(searchService), IUsernameHashedPassword)
    portal.registerChecker(SessionChecker(), ISessionCredentials)

    application = service.Application("Querryl")
    site = server.Site(BasicWrapper(portal, []))
    site.sessionFactory = LongSession

    if ssl:
        ctx = DefaultOpenSSLContextFactory(sslPrivate, sslCert)
        ssl_sv = internet.SSLServer(sslPort, site, ctx, interface=iface)
        ssl_sv.setServiceParent(application)

        if sslRedirect:
            site = server.Site(RedirectFromRequest(port=sslPort))

    sv = internet.TCPServer(port, site, interface=iface)
    sv.setServiceParent(application)
    return sv
