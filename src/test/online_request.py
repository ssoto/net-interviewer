
from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('wtelecom'),
    cmdgen.UdpTransportTarget(('10.200.0.10', 161)),
    '1.3.6.1.4.1.9.9.273.1.2.1.1.16.1.15.87.101.108.108.110.101.115.115.84.101.108.101.99.111.109.0.33.106.108.63.254'
)

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))