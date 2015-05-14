#!/usr/bin/env python

from twisted.internet import reactor, defer
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413.twisted import cmdgen
from pysnmp.carrier.twisted import dispatch
from pysnmp.carrier.twisted.dgram import udp

# Create SNMP engine instance
snmpEngine = engine.SnmpEngine()

# Instantiate and register Twisted dispatcher at SNMP engine
snmpEngine.registerTransportDispatcher(dispatch.TwistedDispatcher())

#
# SNMPv1 setup
#

# SecurityName <-> CommunityName mapping
config.addV1System(snmpEngine, 'my-area', 'public')

# Specify security settings per SecurityName (SNMPv1 - 0, SNMPv2c - 1)
config.addTargetParams(snmpEngine, 'my-creds', 'my-area', 'noAuthNoPriv', 0)

#
# Setup transport endpoint and bind it with security settings yielding
# a target name
#

# UDP/IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTwistedTransport().openClientMode()
)
config.addTargetAddr(
    snmpEngine, 'my-router',
    udp.domainName, ('195.218.195.228', 161),
    'my-creds'
)

# Error/response receiver
def cbFun(cbCtx):
    (errorIndication, errorStatus, errorIndex, varBinds) = cbCtx
    if errorIndication:
        print(errorIndication)
    # SNMPv1 response may contain noSuchName error *and* SNMPv2c exception,
    # so we ignore noSuchName error here
    elif errorStatus and errorStatus != 2:
        print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1][0] or '?'
            )
        )
    else:
        for oid, val in varBinds:
            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

    reactor.stop()

# Prepare request to be sent yielding Twisted deferred object
df = cmdgen.GetCommandGenerator().sendReq(
    snmpEngine,
    'my-router',
    ( ('1.3.6.1.2.1.1.1.0', None), ('1.3.6.1.2.1.1.2.0', None) ),
)

# Register error/response receiver function at deferred
df.addCallback(cbFun)

# Run Twisted main loop
reactor.run()
