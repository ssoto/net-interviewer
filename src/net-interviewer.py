#!/usr/bin/env python
# -*- coding: utf-8 -*-


from snmp.table import SnmpTableRequest
from snmp.factory import SnmpTableFactory
import time
from utils.config_parser import ConfigObject
from utils.threads import StoppableThread
from pprint import pprint
from logstash.udp import Sender

from data.redis_manager import RedisQueue

import logging
logging.basicConfig( 
    format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
    level=logging.DEBUG)

def task ( **kwargs ):
    
    task = SnmpTableFactory.create_request(kwargs)
    

def old_task( **kwargs ):

    OID_req = SnmpTableRequest( server=server, mib_name=mib_name, community=community,oid=oid, port=port)
    try:
        OID_req.request()
    except Exception as excep:
        logging.error("Error on request " + mib_name + '::' + oid)
        logging.error(repr(excep))
        return 1

    OID_req.get_json_reply()


if __name__ == "__main__":

    cf = ConfigObject('./net_interviewer.conf')

    task_list = []

    # create producers threads
    for request in cf.get_requests():
                
        th = StoppableThread(interval=request['interval'], 
                             target=task,
                             kwargs=request)
        
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


