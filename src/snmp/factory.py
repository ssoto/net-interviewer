#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from snmp.table import SnmpTableRequest, SnmpJoinedTableRequest


class SnmpTableFactory(object):

    @classmethod
    def create_request(cls, config):

        if config.has_key('join_oid') and config.has_key('join_extra'):
            logging.debug('created new SnmpJoinedTable request')
            return SnmpJoinedTableRequest(device=config['device'], 
                                          port=config['port'],
                                          community=config['community'],
                                          mib=config['mib'],
                                          oid=config['oid'],
                                          join_oid=config['join_oid'],
                                          join_extra=config['join_extra']
                                           )
        else:
            logging.debug('created new SnmpTable request')
            return SnmpTableRequest(device=config['device'], 
                                    port=config['port'],
                                    community=config['community'],
                                    mib=config['mib'],
                                    oid=config['oid'])

    def generate_request(conf):
        if x:
            return SnmpTableRequest()
        else:
            pass