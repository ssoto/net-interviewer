#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
from utils.config_parser import get_config
from utils.threads import StoppableThread

import logging
logging.basicConfig( 
    format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
    level=logging.DEBUG)

class SNMP_table_thread(StoppableThread, Snmp_table_request):

    def __init__(self, name, host, port, community, snmp_version, mib, oid, interval):
        Snmp_table_request.__init__(server=host, port=port, community=community, 
            snmp_version=snmp_version, mib_name=mib, oid_name=oid)
        StoppableThread.__init__(interval, self.get_json_reply)

    def 
   
def JAJJAJJJAJAJAJJAJAJA (request, ):
    data_dict = { }

    # get all OIDs dicts
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
            logging.error("Error on request " + args.mib_name + '::' + oid)
            logging.error(repr(excep))
            break
        table_dict = OID_req.get_json_reply(args.timestamp_field_name)

    return data_dict

if __name__ == "__main__":

    config_dict = get_config('./net_interviewer.conf')

    devices_config =  { k:v for (k,v) 
            in config_dict.iteritems() if "Daemon-device" in k}

    task_list = []

    for config in  devices_config.values():
        for oid in [item.strip() for item in config['oids'].split(',')]:
            task = SNMP_table_thread( name=config['name'],
                                      host=config['device'],
                                      port=config['port'],
                                      snmp_community=config['community'],
                                      mib=config['mib'],
                                      oid=oid,
                                      interval=int(config['interval']))

            logging.debug("created job %s  with interval %s" %(task.name, task.interval ))

            task_list.append(task)
            task.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        logging.debug("trying exit...")
        for task in task_list:
            task.stop()
            logging.debug("stopping job %s  with interval %s"
                 %(task.name, task.interval ))








