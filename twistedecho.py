from twisted.internet import reactor, protocol

class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        self.transport.write("echo: %s\n"%data)

factory = protocol.ServerFactory()
factory.protocol = Echo
reactor.listenTCP(8080,factory)
print 'waiting for connection...'
reactor.run()
