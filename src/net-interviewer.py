#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Timer
import time
from utils.config_parser import get_config

import logging
logging.basicConfig( format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
                     level=logging.DEBUG)

class SNMP_table_job:

    def __init__(self, name,host,port,snmp_community,mib,oids, interval):
        arguments = locals()
        self.name = name
        self.interval = interval

    def __str__(self):
        import pprint
        pprint.pprint(self.attributes)

    def run(self):
        logging.debug("Task " + self.name + " is working!")

if __name__ == "__main__":

    config_dict = get_config('./net_interviewer.conf')

    devices_config =  { k:v for (k,v) 
            in config_dict.iteritems() 
            if "Daemon-device" in k}

    task_list = []

    for config in  devices_config.values():

        task = SNMP_table_job( name=config['name'],
                              host=config['device'],
                              port=config['port'],
                              snmp_community=config['community'],
                              mib=config['mib'],
                              oids=[item.strip() for item in config['oids'].split(',')],
                              interval=int(config['interval']))

        timer = Timer( int(config['interval']), 
                       task.run, 
                       ())

        logging.debug("created job %s  with interval %s" %(task.name, task.interval ))

        task_list.append([task, timer])
        timer.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        for (task, timer) in task_list:
            timer.cancel()
            logging.debug("stopping job %s  with interval %s" %(task.name, task.interval ))








