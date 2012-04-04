
from twisted.internet import reactor, protocol
from twisted.web.client import getPage


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, line):
        "As soon as any data is received, write it back."
        d = getPage("http://isithackday.com/arrpi.php?text="+line)
        def callback(data):
            self.transport.write("echo: %s\n"%data)
        d.addCallback(callback)

factory = protocol.ServerFactory()
factory.protocol = Echo
reactor.listenTCP(8080,factory)
print 'waiting for connection...'
reactor.run()

