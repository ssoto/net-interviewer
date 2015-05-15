#!/usr/bin/env python
# -*- coding: utf-8 -*-

from table import Snmp_table_request

def do():
    table_req = Snmp_table_request("10.200.0.10", 
                                   "wtelecom", 
                                   "2c",
                                   161,
                                   "CISCO-DOT11-ASSOCIATION-MIB", 
                                   "cDot11ClientConfigInfoTable")
    result = table_req.request()
    #print pprint.pprint(result)

def do_times(times=1000):
    for i in range(0,times):
        do()

if __name__ == "__main__":
    import cProfile
    # 1000000 times: 31.298 seconds
    cProfile.runctx('do_times(10000)', None, locals())
    