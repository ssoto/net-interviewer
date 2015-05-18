snmpwalk -v2c -cwtelecom 10.200.0.16 IF-MIB::ifHCInOctets | grep .10[0-9][0-9[0-9] |awk '{split($1,a,".");print a[2] ";" $4}'
snmpwalk -v2c -cwtelecom 10.200.0.16 IF-MIB::ifHCOutOctets | grep .10[0-9][0-9[0-9] |awk '{split($1,a,".");print a[2] ";" $4}'
snmpwalk -v2c -cwtelecom 10.200.0.16 IF-MIB::ifDescr | grep .10[0-9][0-9[0-9] |awk '{split($1,a,".");print a[2] ";" $4}'
snmptable -v2c -cwtelecom 10.200.0.16 IF-MIB:ifTable