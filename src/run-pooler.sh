nohup python ap-interviewer -s 10.200.0.10 -m CISCO-DOT11-ASSOCIATION-MIB -c wtelecom -o cDot11ClientConfigInfoTable cDot11ClientStatisticTable --ls-host localhost --ls-port 8000  -i 30 > /var/log/snmp-pooler-ap10.log &

nohup python ap-interviewer -s 10.200.0.11 -m CISCO-DOT11-ASSOCIATION-MIB -c wtelecom -o cDot11ClientConfigInfoTable cDot11ClientStatisticTable --ls-host localhost --ls-port 8000  -i 30 > /var/log/snmp-pooler-ap11.log & 
