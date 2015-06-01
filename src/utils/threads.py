#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from time import sleep as time_sleep
from threading import Thread, Event
import random
import re
import socket
from Queue import Empty

from utils.timeutils import times_str_diff
from logstash.udp import Sender

import logging
logging.basicConfig( format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
                     level=logging.DEBUG)

class StoppableTimerThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, interval=None, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        
        Thread.__init__( self, group=None, target=target, name=name, verbose=verbose)
        
        self.__args = args
        self.target = self.__dict__["_Thread__target"]

        self.stop_event = Event()

        self.interval = int(interval)

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()

    def run(self):

        while not self.stop_event.is_set():

            self.stop_event.wait(self.interval)
            if self.stopped():
                return 0
            self.target(*self.__args)

class Memory(object):

    def __init__(self):
        self.__memory = {}
        self.__timestamp_field_name = 'logTimestamp'

    def exist(self, instance_name):
        return self.__memory.has_key(instance_name)

    def get_instance(self, instance_name, field):
        return (self.__memory[instance_name][field],
                self.__memory[instance_name][self.__timestamp_field_name])

    def add_instance(self, instance_name, value):
        self.__memory[instance_name] = value


    def get_timestamp(self, instance_name):
        return self.__memory[instance_name][self.__timestamp_field_name]




class ReaderThread(Thread):


    def __init__(self, queue, send_queue, name):
        super(ReaderThread, self).__init__(name=name)
        self.stop_event = Event()
        self.queue = queue
        self.send_queue = send_queue
        self.__memory = Memory()


    def stop(self):
        self.stop_event.set()


    def stopped(self):
        return self.stop_event.is_set()


    def do_increments(self, elements, incremental_fields):

        new_elements = {}
        elements_to_del = []
        # 1st try
        for key in elements:

            if self.__memory.exist(key):
                # add datediff field
                self.add_datediff(elements, key)

                # the element register exists
                elements_to_add = {}

                for metric in elements[key]:
                
                    if metric in incremental_fields:
                        new_value = elements[key][metric]
                        new_ts = elements[key]['logTimestamp']
                        (old_value, old_ts) = self.__memory.get_instance(key, metric)
                        new_values = self.add_incremental_metrics(metric,
                                                                  new_value,
                                                                  old_value,
                                                                  new_ts, 
                                                                  old_ts)
                        for new_value in new_values:
                            elements_to_add[new_value] = new_values[new_value]
                    # update elements[key] dictioanry
                elements[key].update(elements_to_add)


            else:                
                self.__memory.add_instance(key, elements[key])
                elements_to_del.append(key)

            
        for key in elements_to_del:
            del elements[key]

    def add_incremental_metrics(self, metric_name, new_value, old_value, new_ts, old_ts):

        result = {}
        
        new_ammount = int(re.findall(r'\d+',new_value)[0])
        old_ammount = int(re.findall(r'\d+',old_value)[0])
            
        ammount_diff = new_ammount - old_ammount
        ts_diff = times_str_diff(new_ts, old_ts)

        result[ '%s%s' %(metric_name, 'Diff')] = ammount_diff

        # avoid ZeroDivision try catch
        if ts_diff > 0:
            result[ '%s%s' %(metric_name, 'DiffRate')] = ammount_diff / ts_diff
            

        return result

    def add_datediff(self, elements, instance_name):

        old_ts = self.__memory.get_timestamp(instance_name)
        new_ts = elements[instance_name]['logTimestamp']

        ts_diff = times_str_diff(new_ts, old_ts)
        elements[instance_name]['DeltaTime'] = ts_diff


    def run(self):

        while not self.stop_event.is_set():
            try:
                (elements, incremental_fields) = self.queue.get(True, 1)

                if incremental_fields:
                    self.do_increments(elements, incremental_fields)
                
                if elements:
                    logging.debug('***** adding elements to send_queue')
                    self.send_queue.put(elements)
                else:
                    logging.debug('nothing to send...')

            except Empty:
                pass


class SenderThread(Thread):

    def __init__( self, queue, cfg=None, name=None):
        super(SenderThread, self).__init__(name=name)

        self.queue = queue
        self.stop_event = Event()

        if cfg:
            (self.server, self.port) = cfg


    def stop(self):
        self.stop_event.set()


    def send_message(self, message):
        
        while True:
            try:
                sock = socket.socket(socket.AF_INET, # Internet
                                     socket.SOCK_DGRAM) # UDP
            except socket.error, err:
                time_sleep(1)
                logging.debug("Error sending data: %s" %repr(err))
                pass
            else:
                for element in message:
                    json_dumped = json.dumps(message[element])
                    sock.sendto(json_dumped, 
                                (self.server, self.port))
                sock.close()
                return True


    def run(self):

        while not self.stop_event.is_set():
            try:
                message = self.queue.get(True, 1)
                logging.debug('thread read data from sender queue')
                self.send_message(message)
            except Empty as exception:
                pass
            else:
                logging.debug("***** send message %s ... " %str(message)[0:50])



if __name__ == "__main__":
    
    thread_pool = []

    for i in range(0,10):

        def job(*args, **kwargs):

            print "Hi, I'm %s at %s" %(kwargs['name'], time.ctime())

        r = random.randint(2,5)
        t = StoppableThread( name="Thread-%s" %i,
                             target=job, 
                             interval = r,
                             kwargs={"arg1":"Buenos", 
                                     "arg2":"desayuno",
                                     "name": "Fran"})
        t.start()
        thread_pool.append(t)

    try:
        while True:
            time_sleep(0.5)
            logging.debug("waiting...")
    except KeyboardInterrupt as e:
        for thread in thread_pool:
            logging.debug("killing thread-%s" %thread.name)
            thread.stop()
        logging.error("Exiting!")