#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
from utils.config_parser import get_config
from Queue import Queue

import logging
logging.basicConfig( format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
                     level=logging.DEBUG)

class SNMP_table_job:

    def __init__(self, name,host,port,snmp_community,mib,oids, interval):
        arguments = locals()
        self.name = name
        self.interval = int(interval)

    def start(self):

        self.__timer = threading.Timer(self.interval, self.task).start()

    def stop(self):
        if hasattr(self, "__timer") and self.__timer:
            self.__timer.stop()

    def __str__(self):
        import pprint
        pprint.pprint(self.attributes)


    def task(self):
        logging.debug("Task " + self.name + " is working!")
        self.__timer = threading.Timer(self.interval, self.task).start()


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
            logging.debug("stopping job %s  with interval %s" %(task.name, task.interval ))








