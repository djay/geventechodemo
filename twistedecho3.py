
from twisted.internet import reactor, protocol, defer
from twisted.web.client import getPage
from urllib import urlencode


class Echo(protocol.Protocol):

    @defer.inlineCallbacks
    def dataReceived(self, line):
        data = yield getPage("http://isithackday.com/arrpi.php?"+urlencode({'text':line}))
        self.transport.write("echo: %s\n"%data)

factory = protocol.ServerFactory()
factory.protocol = Echo
reactor.listenTCP(8080,factory)
print 'waiting for connection...'
reactor.run()

