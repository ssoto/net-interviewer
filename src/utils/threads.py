#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from threading import Thread, Event
import random

import logging
logging.basicConfig( format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
                     level=logging.DEBUG)

class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, interval=None, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        
        Thread.__init__( self, group=None, target=target, name=name, verbose=verbose)
        
        self.__kwargs = kwargs
        self.__args = args
        self.target = self.__dict__["_Thread__target"]

        self.stop_event = Event()

        self.interval = int(interval)

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.isSet()

    def run(self):

        while not self.stop_event.is_set():

            self.stop_event.wait(self.interval)
            if self.stopped():
                return 0
            self.target(*self.__args, **self.__kwargs)


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