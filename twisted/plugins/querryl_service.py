from zope.interface import implements

from twisted.python import usage
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin

from querryl.deployment import deploy



class QuerrylServiceMaker(object):
    implements(IPlugin, IServiceMaker)
    tapname = 'querryl'
    description = 'Quassel searching web application'
    options = usage.Options

    def makeService(self, options):
        config = {}
        exec file('config.py', 'rb') in config
        del config['__builtins__']
        return deploy(**config)

serviceMaker = QuerrylServiceMaker()
