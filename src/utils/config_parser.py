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
        cfg = ConfigParser.ConfigParser()
        cfg.read(config_file_path)
        self.__options_dict = {}
        
        self.config = {
            SNMP_TABLES : [],
            SNMP_JOIN_TABLE : []
        }

        for section in cfg.sections():
            if section.startswith('SNMP-table-'):
                element = {
                    'name' : cfg.get(section, 'name'),
                    'device' : cfg.get(section, 'device'),
                    'port' : cfg.getint(section, 'port'),
                    'interval' : cfg.getint(section, 'interval'),
                    'community' : cfg.get(section, 'community'),
                    'mib' : cfg.get(section, 'mib'),
                    'oid' : cfg.get(section, 'oid'),
                    'incremental_fields': self.get_extra_fields(cfg, section, 'incremental_fields')
                }

                self.config[SNMP_TABLES].append(element)

            elif section.startswith('SNMP-join-table'):
                element = {
                    'name' : cfg.get(section, 'name'),
                    'device' : cfg.get(section, 'device'),
                    'port' : cfg.getint(section, 'port'),
                    'interval' : cfg.getint(section, 'interval'),
                    'community' : cfg.get(section, 'community'),
                    'mib' : cfg.get(section, 'mib'),
                    'oid' : cfg.get(section, 'oid'),
                    'join_oid' : cfg.get(section, 'join_oid'),
                    'field_to_join': cfg.get(section, 'field_to_join'),
                    'join_extra' : cfg.get(section, 'join_extra').split(','),
                    'incremental_fields': self.get_extra_fields(cfg, section, 'incremental_fields')
                }
                self.config[SNMP_JOIN_TABLE].append(element)
            else:
                logging.error('undefined field in configuration file: %s' %section)
                raise AttributeError('error field in configuration file: %s' %section)

    def get_extra_fields(self, cfg, section, name):
        """
            (...)
            incremental_fields = field1, field2, field3
            (...)
        """
        raw = cfg.get(section,name)
        return [field.strip() for field in raw.split(',')]


    def get_requests(self):
        return list(self.config[SNMP_TABLES] + self.config[SNMP_JOIN_TABLE])

    def get_snmp_table_requests(self):

        return self.config[SNMP_TABLES]

    def get_snmp_join_table_requests(self):
        
        return self.config[SNMP_JOIN_TABLE]        


if __name__ == "__main__":
    import pprint
    cf = ConfigObject('./net_interviewer.conf')
    import ipdb; ipdb.set_trace()
    cf.get_prop('Data', 'timestamp_field_name')
    print cf.get_requests()
