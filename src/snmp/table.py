#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import pytz
import re
import subprocess

class Snmp_table_request:
    """
    Example of how could be a generic snmp table request

    options are 

    """
    def __init__ (self, server, port=161, community="public", snmp_version="2c", mib_name=None, oid_name=None, cmd_options=None):
        
        default_arguments = "-Cf", ",", "-Cl", "-CB", "-Ci", "-OX", "-Cb", "-Oe"
        
        self.server = server
        self.port = port
        self.community = community
        self.snmp_version = snmp_version
        self.mib_name = mib_name
        self.oid_name = oid_name
        self.__cmd = ["snmptable",
                     "-v",
                     snmp_version,
                     "-c",
                     community, 
                     server]

        self.__cmd.extend(default_arguments)
        self.__cmd.append(mib_name + ":" + oid_name)
        command_str = ' '.join(map(str, self.__cmd))
        logging.info("new rquest created: "+ command_str)

    def __get_current_time(self):

        utc = pytz.utc
        fmt = '%Y-%m-%d %H:%M:%S %z'
        madrid_tz = pytz.timezone('Europe/Madrid')

        dt = datetime.datetime.now()
        madrid_dt = madrid_tz.localize(dt)
        return madrid_dt.astimezone(utc).strftime(fmt)

    def request(self, simulate=False):    
        self.__timestamp = self.__get_current_time()
        logging.debug('timestamp local: %s' % self.__timestamp)
        try:
            self.raw_output = subprocess.check_output(self.__cmd)
        except Exception as call_error:
            logging.error("Error doing request")
            raise

    def get_json_reply(self):
        if hasattr(self, 'json_output'):
            return self.json_output
        elif not hasattr(self, 'raw_output'):
            raise AttributeError('request output has not been established... Request has not been done or failed')
        else:
            tmp_list = [ x.split(',') for x in self.raw_output.split('\n') ]
            # delete first 2 lines, an inroduccion message for the MIB
            output_list = tmp_list[2:]
            
            header = output_list[0]
            rows = output_list[1:-1]

            self.json_output = self._get_body_dict(header, rows)

            return self.json_output

    def _get_body_dict(self, header, elements):

        result = {}

        num_rows = len(elements)
        num_colums = len(header)
        
        prog = re.compile( r"\[([a-zA-Z0-9_:]+)\]\[([a-zA-Z0-9_:]+)\]\[([a-zA-Z0-9_:]+)\]")
        
        for i in range(0, num_rows):
            element_dict = {}
            for j in range(0, num_colums):
                element_dict[header[j]] = (elements[i][j]).translate(None, '"').strip()
            m = prog.match(element_dict['index'])

            (num_id, ssid, mac_address) = m.groups()
            element_dict['MacAddress'] = mac_address
            element_dict['SSIDName'] = ssid
            element_dict['logTimestamp'] = self.__timestamp

            #manage dictionary key. I'm going to use the MAC to search after
            result[mac_address] = element_dict
        return result