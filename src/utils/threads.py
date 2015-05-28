#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import logging
import random

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, interval, job):
        super(StoppableThread, self).__init__()
        self.stop_event = threading.Event()

        self.interval = interval
        self.job = job

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.isSet()

    def run(self):

        logging.debug("running thread...")
        self._remainning = self.interval

        while not self.stop_event.is_set():

            self.stop_event.wait(self.interval)
            if self.stopped():
                return 0
            self.job(self.name)

if __name__ == "__main__":
    
    thread_pool = []

    for i in range(0,10):

        def job(name):
            print "Hi, I'm %s and it's %s" %(name, time.ctime())

        r = random.randint(10,20)
        t = StoppableThread(r, job)
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