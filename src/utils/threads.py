#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from threading import Thread, Event
import random
import re
from Queue import Empty

from utils.time import times_str_diff

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

    def exist(self, tag):
        return self.__memory.has_key(tag)

    def get_instance(self, instance_name, field):
        return (self.__memory[instance_name][field],
                self.__memory[instance_name]['logTimestamp'])

    def add_instance(self, instance_name, value):
        
        self.__memory[instance_name] = value




class ReaderThread(Thread):

    def __init__(self, queue):
        super(ReaderThread, self).__init__()
        self.stop_event = Event()
        self.queue = queue
        self.__memory = Memory()

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()

    def do_increments(self, elements, incremental_fields, delta_time):

        new_elements = {}
        elements_to_del = []
        # 1st try
        for key in elements:
            if self.__memory.exist(key):

                # the element register exists
                elements_to_add = {}

                for metric in elements[key]:
                
                    if metric in incremental_fields:
                        new_value = elements[key][metric]
                        new_ts = elements[key]['logTimestamp']
                        (old_value, old_ts) = self.__memory.get_instance(key, metric)
                        new_values = self.get_metrics(metric,
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

    def get_metrics(self, metric_name, new_value, old_value, new_ts, old_ts):

        result = {}
        
        new_ammount = int(re.findall(r'\d+',new_value)[0])
        old_ammount = int(re.findall(r'\d+',old_value)[0])
            
        ammount_diff = new_ammount - old_ammount
        ts_diff = times_str_diff(new_ts, old_ts)

        result[ '%s%s' %(metric_name, 'Diff')] = ammount_diff

        # avoid ZeroDivision try catch
        if ts_diff > 0:
            result[ '%s%s' %(metric_name, 'DiffRate')] = ammount_diff / ts_diff
            result[ '%s%s' %(metric_name, 'DeltaTime')] =  ts_diff

        return result


    def run(self):

        while not self.stop_event.is_set():
            try:
                (elements, incremental_fields) = self.queue.get(True, 0.5)
                if incremental_fields:
                    self.do_increments(elements, incremental_fields)
                logging.debug("do increments on %s of %s" 
                    %(elements, incremental_fields))
            except Empty:
                pass




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
            time.sleep(0.5)
            logging.debug("waiting...")
    except KeyboardInterrupt as e:
        for thread in thread_pool:
            logging.debug("killing thread-%s" %thread.name)
            thread.stop()
        logging.error("Exiting!")