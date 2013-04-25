from zope.interface import Interface, Attribute, implements

from twisted.python.components import registerAdapter
from twisted.web.server import Session


class IUserStorage(Interface):
    name = Attribute("A user's name.")
    userid = Attribute("userid.")



class UserStorage(object):
    implements(IUserStorage)

    def __init__(self, session):
        self.userid = None
        self.name = ''


registerAdapter(UserStorage, Session, IUserStorage)
