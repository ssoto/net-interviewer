#!/usr/bin/env python
# -*- coding: utf-8 -*-

from snmp.table import Snmp_table_request
import pprint


if __name__ == '__main__':

    ip = '10.200.0.10'
    community = 'wtelecom'
    version = '2c'
    port = 161
    cisco_DOT11 = 'CISCO-DOT11-ASSOCIATION-MIB'
    config_table_OID = 'cDot11ClientConfigInfoTable'
    statistic_table = 'cDot11ClientStatisticTable'


    config_table_OID_req = Snmp_table_request(server = ip, 
                                   community = community, 
                                   snmp_version = version,
                                   port = port,
                                   mib_name = cisco_DOT11, 
                                   oid_name = config_table_OID)
    config_table_OID_req.request()
    table_dict = config_table_OID_req.get_json_reply()
    pprint.pprint(table_dict)

    statistic_table_OID_req = Snmp_table_request(server = ip, 
                                   community = community, 
                                   snmp_version = version,
                                   port = port,
                                   mib_name = cisco_DOT11, 
                                   oid_name = statistic_table)
    statistic_table_OID_req.request()

    statistic_dict = statistic_table_OID_req.get_json_reply()
    pprint.pprint(statistic_dict)
    import pdb; pdb.set_trace() #BREAKPOINT 
    