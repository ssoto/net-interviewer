#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from ConfigParser import NoOptionError
from Queue import Queue
import sys
import time

from interviewer.snmp.table import SnmpTableRequest
from interviewer.snmp.factory import SnmpTableFactory
from interviewer.utils.config_parser import ConfigObject
from interviewer.utils.threads import StoppableTimerThread, ReaderThread, SenderThread

import logging


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', dest='config_path',
                        default='./net_interviewer.conf', action='store',
                        help='the file config path to read')

    parser.add_argument('-d', '--debug', dest='debug_mode', 
                        action='store_true', default=False,
                        help='activate debug mode')

    return parser.parse_args()


def task (queue, rq_config):

    job = SnmpTableFactory.create_request(rq_config)
    try:
        job.request()
    except Exception as e:
        logging.error('error in call to %s: %s' %(job.device, repr(e)))
        return
    
    
    data = job.get_json_reply()
    
    import ipdb, pprint; ipdb.set_trace()

    if rq_config['incremental_fields']:
       incremental_fields = rq_config['incremental_fields']
    else:
        incremental_fields = None

    # on the develop moment only one custom_field is needed: device_id
    custom_fields = {}
    # consider the name difference camel case vs _ separator
    custom_fields['DeviceId'] = rq_config['device_id']

    queue.put((data, incremental_fields, custom_fields))

    logging.debug('request done succesfully to %s: %s' 
        %(job.device, str(data)[0:30]))


if __name__ == "__main__":

    args = parse_args()

    try:
        cf = ConfigObject(args.config_path)
    except NoOptionError as e:
        logging.error("error in config file: %s" %repr(e))
        sys.exit(0)

    if args.debug_mode:
        logging.basicConfig( 
            format='%(asctime)s - %(pathname)s:%(lineno)d - %(threadName)s : %(levelname)s  : %(message)s', 
            level=logging.DEBUG)
    else:
        logging.basicConfig( 
            format='%(asctime)s - %(pathname)s:%(lineno)d - %(threadName)s : %(message)s', 
            level=logging.ERROR)


    task_list = []
    raw_data_queue = Queue()
    send_queue = Queue()

    r_th = ReaderThread(raw_data_queue, send_queue, name='ReaderThread')
    r_th.start()
    
    output_config = cf.get_output_section()
    
    s_th = SenderThread(send_queue, output_config, name='SenderThread')
    s_th.start()

    task_list.append(r_th)
    task_list.append(s_th)


    # create producers threads
    for rq_config in cf.get_requests():
        th = StoppableTimerThread(interval=rq_config['interval'], 
                                 target=task,
                                 name='%s-RequestThread' %rq_config['name'],
                                 args=(raw_data_queue, rq_config),)
        th.start()
        task_list.append(th)

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt as e:
        logging.critical("time to say goobye...")
        # unexpected behaviour
    except Exception as e:
            logging.critical("unexpected Exception captured in main: %s" %repr(e))

    finally:
        for task in task_list:
            task.stop()
            logging.critical("stopping %s"
                 %(task.name ))
        