
from twisted.internet import reactor, protocol
from twisted.web.client import getPage
from urllib import urlencode


class Echo(protocol.Protocol):

    def dataReceived(self, line):
        d = getPage("http://isithackday.com/arrpi.php?"+urlencode({'text':line}))
        def callback(data):
            self.transport.write("echo: %s\n"%data)
        d.addCallback(callback)

factory = protocol.ServerFactory()
factory.protocol = Echo
reactor.listenTCP(8080,factory)
print 'waiting for connection...'
reactor.run()

