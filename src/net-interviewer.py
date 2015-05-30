#!/usr/bin/env python
# -*- coding: utf-8 -*-

from snmp.table import SnmpTableRequest
import threading
import time
from utils.config_parser import get_config
from utils.threads import StoppableThread
from pprint import pprint

import logging
logging.basicConfig( 
    format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
    level=logging.DEBUG)

def generate_config(config_file_path):

    config_dict = get_config(config_file_path)
    
    devices_config =  { k:v for (k,v) 
            in config_dict.iteritems() if "Daemon-device" in k}

    requests = []

    for config in  devices_config.values():
        for oid in [item.strip() for item in config['oids'].split(',')]:
            for server in [item.strip() for item in config['device'].split(',')]:
                kwargs = {
                    'oid': oid,
                    'server': server,
                    'community': config['community'],
                    'port': config['port'],
                    'mib_name': config['mib']
                }
                requests.append(kwargs)
    return (config, requests)


def task( server, community, port, mib_name, oid):

    OID_req = SnmpTableRequest( server=server, mib_name=mib_name, community=community,oid=oid, port=port)
    try:
        OID_req.request()
    except Exception as excep:
        logging.error("Error on request " + config['mib'] + '::' + oid)
        logging.error(repr(excep))

    OID_req.get_json_reply()


if __name__ == "__main__":

    (config, requests) = generate_config('./net_interviewer.conf')

    task_list = []
    
    for request in requests:
        th = StoppableThread(interval=config['interval'], 
                             target=task,
                             kwargs=request)

        logging.debug("created new thread to process %s::%s to %s" 
            %(request['mib_name'], request['oid'], request['server']))
        th.start()
        task_list.append(th)

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        
        logging.debug("trying exit...")

        for task in task_list:
            task.stop()
            logging.debug("stopping job %s  with interval %s"
                 %(task.name, task.interval ))


