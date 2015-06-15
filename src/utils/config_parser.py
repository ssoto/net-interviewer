#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import logging
logging.basicConfig( format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
                     level=logging.DEBUG)


SNMP_TABLES = 'SNMP-table'
SNMP_JOIN_TABLE = 'SNMP-join-table'

class ConfigObject:
    
    def __init__(self, config_file_path):
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(config_file_path)
        self.__options_dict = {}
        
        self.config = {
            SNMP_TABLES : [],
            SNMP_JOIN_TABLE : []
        }

        for section in self.cfg.sections():
            if section.startswith('SNMP-table-'):
                element = {
                    'name' : self.cfg.get(section, 'name'),
                    'device' : self.cfg.get(section, 'device'),
                    'port' : self.cfg.getint(section, 'port'),
                    'interval' : self.cfg.getint(section, 'interval'),
                    'community' : self.cfg.get(section, 'community'),
                    'mib' : self.cfg.get(section, 'mib'),
                    'oid' : self.cfg.get(section, 'oid'),
                    'device_id': self.cfg.get(section, 'device_id'),
                    'incremental_fields': self.get_extra_fields(section, 'incremental_fields')
                }

                self.config[SNMP_TABLES].append(element)

            elif section.startswith('SNMP-join-table'):
                element = {
                    'name' : self.cfg.get(section, 'name'),
                    'device' : self.cfg.get(section, 'device'),
                    'port' : self.cfg.getint(section, 'port'),
                    'interval' : self.cfg.getint(section, 'interval'),
                    'community' : self.cfg.get(section, 'community'),
                    'mib' : self.cfg.get(section, 'mib'),
                    'oid' : self.cfg.get(section, 'oid'),
                    'join_oid' : self.cfg.get(section, 'join_oid'),
                    'field_to_join': self.cfg.get(section, 'field_to_join'),
                    'device_id': self.cfg.get(section, 'device_id'),
                    'join_extra' : self.cfg.get(section, 'join_extra').split(','),
                    'incremental_fields': self.get_extra_fields( section, 'incremental_fields')
                }
                self.config[SNMP_JOIN_TABLE].append(element)
            

    def get_output_section(self):
        """ 
        Return the 'Output' section of the config file
        """
        section = 'Output'
        return (
            self.cfg.get(section, 'server'),
            self.cfg.getint(section, 'port')
        )



    def get_extra_fields(self, section, name):
        """
            (...)
            incremental_fields = field1, field2, field3
            (...)
        """
        raw = self.cfg.get(section,name)
        result = [field.strip() for field in raw.split(',')]
        if result:
            return result
        else:
            return None


    def get_requests(self):
        return list(self.config[SNMP_TABLES] + self.config[SNMP_JOIN_TABLE])

    def get_snmp_table_requests(self):

        return self.config[SNMP_TABLES]

    def get_snmp_join_table_requests(self):
        
        return self.config[SNMP_JOIN_TABLE]        

if __name__ == "__main__":

    from sys import argv

    try:

        cf = ConfigObject(argv[1])

    except ConfigParser.NoOptionError as e:

        logging.error("error in config file: %s" %repr(e))
    else:
        print cf.get_requests()