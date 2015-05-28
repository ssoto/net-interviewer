#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
import logging
import re
import subprocess
import StringIO

from utils.time import get_current_time

class Snmp_table_request:
    """
    Example of how could be a generic snmp table request

    options are 

    """
    def __init__ (self, server, port=161, community="public", snmp_version="2c", 
        mib_name=None, oid_name=None, cmd_options=None):
        
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

    
    def request(self, simulate=False):

        self.__timestamp = get_current_time()
        logging.debug('timestamp local: %s' % self.__timestamp)
        try:
            self.raw_output = subprocess.check_output(self.__cmd)
        except Exception as call_error:
            logging.error("Error doing request")
            raise

    def get_json_reply(self, index_field_name=None, timestamp_field_name='@timestamp'):
        """
        Argument timestamp_field_name will give the name of the field where
        the received timestamp will be wrote
        """
        if hasattr(self, 'json_output'):
            return self.json_output
        elif not hasattr(self, 'raw_output'):
            raise AttributeError('request output has not been established... Request has not been done or failed')
        else:
            self.data_dict = self.parse_csv_string(self.raw_output,
                                                   index_field_name,
                                                   timestamp_field_name)
            return self.data_dict

    def parse_csv_string(self, scsv, index_field_name=None, timestamp_field_name=None):

        result = {}

        f = StringIO.StringIO(scsv)

        reader = csv.reader(f, delimiter=',')

        # drop first two lines, appended by snmptable command and useless for us
        reader.next()
        reader.next()

        header = reader.next()

        if not index_field_name:
            index_field_name = header[0]
        

        for row in reader:
            instance = {}

            for index in range(0,len(row)):
                instance [header[index]] = row[index]
            instance[timestamp_field_name] = self.__timestamp
            
            result[instance[index_field_name]] = instance

        return result

    def _get_body_dict(self, header, elements, timestamp_name, index_field_name):

        result = {}

        num_rows = len(elements)
        num_colums = len(header)
        
        prog = re.compile( r"\[([a-zA-Z0-9_:]+)\]\[([a-zA-Z0-9_:]+)\]\[([a-zA-Z0-9_:]+)\]")
        
        for i in range(0, num_rows):
            element_dict = {}
            for j in range(0, num_colums):
                element_dict[header[j]] = (elements[i][j]).translate(None, '"').strip()


            m = prog.match(element_dict['index'])
            if m:
                (num_id, ssid, mac_address) = m.groups()
                element_dict['MacAddress'] = mac_address
                element_dict['SSIDName'] = ssid
                
            element_dict[timestamp_name] = self.__timestamp

            #manage dictionary key. I'm going to use the MAC to search after
            result[mac_address] = element_dict
        return result



