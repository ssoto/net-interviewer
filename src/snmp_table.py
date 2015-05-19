#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from snmp.table import Snmp_table_request
from sys import argv
from pprint import pprint

from utils.ip_manager import get_decimal_ip


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port', dest='port',
                        default='161', action='store',
                        help='port to send snmp command')

    parser.add_argument('-s', '--server', dest='server', required=True,
                        help='server to send snmp command')

    parser.add_argument('-c', '--community', dest='community', required=True,
                        help='snmp community field')

    parser.add_argument('-sv', '--snmpversion', dest='snmp_version', default='2c',
                        help='snmp version')

    parser.add_argument('-m', '--mib-name', dest='mib_name', required=True,
                        help='mib name')

    parser.add_argument('-o', '--oids', required=True,
                        type=str, nargs='+',
                        dest='oids',  help='list of oids')

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()

    for oid in args.oids:

        OID_req = Snmp_table_request(server = args.server, 
                                       community = args.community, 
                                       snmp_version = args.snmp_version,
                                       port = args.port,
                                       mib_name = args.mib_name, 
                                       oid_name = oid)
        OID_req.request()
        table_dict = OID_req.get_json_reply()
        
        if table_dict[0].has_key('IpAddress'):
            for index in table_dict:
                element = table_dict[index]
                element['IpAddress'] = get_decimal_ip(element['IpAddress'])

        print args.mib_name+"::"+oid
        pprint (table_dict)

        print ('===================================================')

    