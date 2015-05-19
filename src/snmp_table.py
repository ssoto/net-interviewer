#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import os
from pprint import pprint
from snmp.table import Snmp_table_request
from sys import argv

from utils.ip_manager import get_decimal_ip, append_field
from utils.color_print import error, success


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port', dest='port',
                        default='161', action='store',
                        help='port to send snmp command')

    parser.add_argument('-s', '--server', dest='server', required=True,
                        help='server to send snmp command')

    parser.add_argument('-c', '--community', dest='community', required=True,
                        help='snmp community field')

    parser.add_argument('-sv', '--snmpversion', dest='snmp_version', 
                        default='2c', help='snmp version')

    parser.add_argument('-m', '--mib-name', dest='mib_name', required=True,
                        help='mib name')

    parser.add_argument('-o', '--oids', required=True,
                        type=str, nargs='+',
                        dest='oids',  help='list of oids')

    parser.add_argument('-w', '--write_output', dest='file_path',
                        help='if passed, snmp output are writed on the file')
    
    args_parsed = parser.parse_args()

    # check file to output to print
    if hasattr(args_parsed, 'file_path') and os.path.isfile(args_parsed.file_path):
        try: 
            open(args_parsed.file_path)
        except IOError as e:
            error("Error with file to write request output: " + args_parsed.file_path)
            sys.exit(0)
    
    return args_parsed


def write_on_file (file_name, object_data):
    with open(file_name+'.json', 'w') as outfile:
        json.dump(object_data, outfile, indent=2)

if __name__ == '__main__':

    args = parse_args()
    data_dict = {}

    for oid in args.oids:

        OID_req = Snmp_table_request( server = args.server, 
                                     community = args.community, 
                                     snmp_version = args.snmp_version,
                                     port = args.port,
                                     mib_name = args.mib_name, 
                                     oid_name = oid)
        try:
            OID_req.request()
        except Exception as excep:
            error("Error on request " + args.mib_name + '::' + oid )
            break
        table_dict = OID_req.get_json_reply()
        
        if oid == 'cDot11ClientConfigInfoTable':
            for index in table_dict:
                element = table_dict[index]
                element['IpAddress'] = get_decimal_ip(element['IpAddress'])
        
        mib_oid_name = args.mib_name+"::"+oid 
        
        data_dict[mib_oid_name] = table_dict
        write_on_file(mib_oid_name, table_dict)

    # add ip field from 
    append_field(data=data_dict, 
                 original_ds='CISCO-DOT11-ASSOCIATION-MIB::cDot11ClientConfigInfoTable',
                 destination_ds='CISCO-DOT11-ASSOCIATION-MIB::cDot11ClientStatisticTable',
                 field='IpAddress')

    output_file = "./output_test"
    success("Request done successfully, output json writed on " + args.file_path)
    write_on_file( file_name="./output_test", 
                   object_data = data_dict["CISCO-DOT11-ASSOCIATION-MIB::cDot11ClientStatisticTable"])

    