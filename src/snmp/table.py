#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
import logging
import re
import subprocess
import StringIO

from utils.time import get_current_time

class SnmpTableRequest(object):
    """
    Example of how could be a generic snmp table request

    options are 

    """
    def __init__ (self, device, port=161, community="public", snmp_version="2c", 
        mib=None, oid=None, cmd_options=None):

        default_arguments = "-Cf", ",", "-Cl", "-CB", "-Ci", "-OX", "-Cb", "-Oe"
        
        self.device = device
        self.port = int(port)
        self.community = community
        self.snmp_version = snmp_version
        self.mib = mib
        self.oid_name = oid
        self.__cmd = ["snmptable",
                     "-v",
                     snmp_version,
                     "-c",
                     community, 
                     device]

        self.__timestamp_field_name = "logTimestamp"
        self.__cmd.extend(default_arguments)
        self.__cmd.append("%s:%s" %(self.mib, self.oid_name))
        
        command_str = ' '.join(map(str, self.__cmd))
        logging.info("new request created: \n\t%s" % command_str)

    
    def request(self, simulate=False):

        self.__timestamp = get_current_time()
    
        self.raw_output = subprocess.check_output(self.__cmd)
        

    def get_json_reply(self, index_field_name=None):
        """
        Argument timestamp_field_name will give the name of the field where
        the received timestamp will be wrote
        """
        
        if hasattr(self, 'json_output'):
            return self.json_output
        elif not hasattr(self, 'raw_output'):
            raise AttributeError('request output has not been established... '
                'Request has not been done or failed')
        else:

            data_dict = self.parse_csv_string(self.raw_output,
                                                   index_field_name)

            return data_dict

    def parse_csv_string(self, scsv, index_field_name=None):

        result = {}

        f = StringIO.StringIO(scsv)

        reader = csv.reader(f, delimiter=',')

        # drop first two lines, appended by snmptable command and useless 4 us
        reader.next()
        reader.next()

        header = reader.next()

        if not index_field_name:
            index_field_name = header[0]
        

        for row in reader:
            instance = {}

            for index in range(0,len(row)):
                instance [header[index]] = row[index]
            instance[self.__timestamp_field_name] = self.__timestamp
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


class SnmpJoinedTableRequest(SnmpTableRequest):

    def __init__(self, device, port=161, community="public", snmp_version="2c", 
        mib=None, oid=None, cmd_options=None, join_oid=None, field_to_join=None,
         join_extra=None):
        
        super(SnmpJoinedTableRequest, self).__init__(device=device, port=port, 
            community=community, snmp_version=snmp_version, mib=mib, oid=oid, 
            cmd_options=cmd_options)

        self.__joined_table_req = SnmpTableRequest(device=device, port=port, 
            community=community, snmp_version=snmp_version, mib=mib, 
            oid=join_oid)

        
        self.__join_extra = [element.strip() for element in join_extra]

        
    def request(self, simulate=False):
        """

        """
        super(SnmpJoinedTableRequest, self).request()
        self.__joined_table_req.request()


    def get_json_reply(self):

        original = super(SnmpJoinedTableRequest, self).get_json_reply()
        join = self.__joined_table_req.get_json_reply()

        for index in original:
            
            for k in self.__join_extra:
                try:
                    value = join[index][k]
                    original[index][k] = value
                except KeyError as e:
                    logging.info("device %s not present in statistic dataset: %s" %( index, repr(e)))
                    pass
        
        return original

