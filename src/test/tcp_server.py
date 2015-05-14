#!/usr/bin/env python

from twisted.internet import protocol, reactor, endpoints

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

if __name__ == "__main__":
    endpoints.serverFromString(reactor, "tcp:1234").listen(EchoFactory())
    reactor.run()