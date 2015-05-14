#!/bin/python

from pysnmp.entity.rfc3413.oneliner import cmdgen

def cbFun(sendRequestHandle, errorIndication, errorStatus, errorIndex,
          varBinds, cbCtx):
    if errorIndication:
        print(errorIndication)
        return
    if errorStatus:
        print('%s at %s' % \
            (errorStatus.prettyPrint(),
             errorIndex and varBinds[int(errorIndex)-1] or '?')
        )
        return
    
    for oid, val in varBinds:
        if val is None:
            print(oid.prettyPrint())
        else:
            print('----------------------------------------------------------')
            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
            print('----------------------------------------------------------')

cmdGen  = cmdgen.AsynCommandGenerator()

queryMibs = (('SNMPv2-MIB', 'sysDescr', 0),
             ('SNMPv2-MIB', 'sysLocation', 0),
             ('SNMPv2-MIB', 'sysName', 0),
             
             ('SNMPv2-MIB', 'cDot11ActiveWirelessClients', 0),
             #('SNMPv2-MIB', 'cDot11ClientCurrentTxRateSet', 0)
             #('SNMPv2-MIB', 'cDot11ClientIpAddress', 0)
             #('SNMPv2-MIB', 'oriStationStatTableIPAddress', 0)
             #('SNMPv2-MIB', 'cDot11ClientName', 0)
             #('SNMPv2-MIB', 'cDot11ClientSignalStrength', 0)
             #('SNMPv2-MIB', 'cDot11ClientSigQuality', 0)
             #('SNMPv2-MIB', 'cDot11ClientUpTime', 0)
             )

for (snmp_version, mib_name, ident) in queryMibs:
    mib_instance = cmdgen.MibVariable(snmp_version, mib_name, ident)
    
    try:
        cmdGen.getCmd(
            cmdgen.CommunityData('wtelecom'),
            cmdgen.UdpTransportTarget(('10.200.0.10', 161)),
            #cmdgen.UdpTransportTarget(('127.0.0.1', 1161)),
            (mib_instance,),
            (cbFun, None)
        )
    except Exception, e:
        print e
        

cmdGen.snmpEngine.transportDispatcher.runDispatcher()