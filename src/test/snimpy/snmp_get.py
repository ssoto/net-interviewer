#!/bin/python

from snimpy.manager import Manager as M
from snimpy.manager import load
import sys

host = "10.200.0.10"
wt_community = "wtelecom"

def get_description ():
    load("IF-MIB")
    
    print ("================================\nIF-MIB:ifDescr")
    
    m = M( host=host, community=wt_community)
    ifDescr = m.ifDescr
    for index in ifDescr:
        print repr(ifDescr[index])

def get_cisco_clientIpAddress():

    CISCO_MIBS_PATH = "/var/lib/mibs/cisco/"
    
    load(sys.path.apend(CISCO_MIBS_PATH, "CISCO-SMI"))
    load(sys.path.apend(CISCO_MIBS_PATH, "IEEE802dot11-MIB"))
    load(sys.path.apend(CISCO_MIBS_PATH, "CISCO-DOT11-IF-MIB"))
    load(sys.path.apend(CISCO_MIBS_PATH, "CISCO-DOT11-ASSOCIATION-MIB"))
    
    m = M ( host=host, community=wt_community)

    oids = ( 
            # 'cDot11AssStatsAssociated',
            #    'cDot11AssStatsAuthenticated',
            #    'cDot11AssStatsRoamedIn',
            #    'cDot11AssStatsRoamedAway',
            #    'cDot11AssStatsDeauthenticated',
            #    'cDot11AssStatsDisassociated',
             'cDot11ClientConfigInfoTable',
           )


    for oid in oids:
        import ipdb; ipdb.set_trace() #BREAKPOINT
        print "==============================\n::", oid
        associated_info = getattr(m, oid)
        for value in associated_info:
            print "\t", oid, "::", value, associated_info[value]


if __name__ == "__main__":

    #get_description()

    get_cisco_clientIpAddress()