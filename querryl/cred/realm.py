from zope.interface import implements

from twisted.cred.portal import IRealm
from twisted.web import static
from twisted.web.resource import IResource, Resource

from querryl.resources import LoginPage, SearchRoot, GetBlock, Search


class PublicHTMLRealm(object):
    implements(IRealm)

    def __init__(self,  search):
        self.search = search


    def anonymous(self):
        root = Resource()
        root.putChild("", LoginPage(self.avatarId))
        root.putChild("login", LoginPage(self.avatarId))
        root.putChild("static", static.File('querryl/static/'))
        return root


    def registered(self):
        root = Resource()
        root.putChild("", SearchRoot(self.avatarId, self.search))
        root.putChild("search", Search(self.avatarId, self.search))
        root.putChild("block", GetBlock(self.avatarId, self.search))
        root.putChild("login", LoginPage(self.avatarId))
        root.putChild("static", static.File('querryl/static/'))
        return root


    def requestAvatar(self, avatarId, mind, *interfaces):
        self.avatarId = avatarId
        if IResource in interfaces:
            if avatarId:
                return (IResource, self.registered(), lambda: None)
            else:
                return (IResource, self.anonymous(), lambda: None)
        raise NotImplementedError()
