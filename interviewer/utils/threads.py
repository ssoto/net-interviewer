#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import json
import logging
import pprint
import re
import socket
from time import sleep as time_sleep
from threading import Thread, Event
from Queue import Queue, Empty

from interviewer.utils.timeutils import times_str_diff
from interviewer.utils.ip_manager import get_decimal_ip


class StoppableTimerThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, interval=None, group=None, target=None, name=None, 
        args=(), kwargs=None, verbose=None):
        
        Thread.__init__( self, group=None, target=target, name=name, 
            verbose=verbose)
        
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

            if self.stopped():
                return 0
            self.target(*self.__args)

            self.stop_event.wait(self.interval)


class Memory(object):
    """

    """

    def __init__(self):
        self.__memory = {}
        self.__timestamp_field_name = 'logTimestamp'

    def exist(self, instance_name):
        return self.__memory.has_key(instance_name)

    def get_instance(self, instance_name, field):
        return (self.__memory[instance_name][field],
                self.__memory[instance_name][self.__timestamp_field_name])

    def set_instance(self, instance_name, value):
        self.__memory[instance_name] = value


    def get_timestamp(self, instance_name):
        return self.__memory[instance_name][self.__timestamp_field_name]

    def __repr__(self):
        from pprint import pformat
        return pformat(self.__memory)


class ReaderThread(Thread):


    def __init__(self, queue, send_queue, name, memory=None):
        if not queue or not send_queue or not name:
            raise TypeError
        super(ReaderThread, self).__init__(name=name)
        self.stop_event = Event()
        self.input_queue = queue
        self.send_queue = send_queue
        if not memory:
            self.__memory = Memory()
        else:
            self.__memory = memory

        self.__mapping = { 'IpAddress': get_decimal_ip }
        self.__bandwidth_fields_set = \
                set(['DeltaTime', 'OutOctetsDiff', 'InOctetsDiff', 'Speed'])

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()


    def do_increments(self, elements, incremental_fields):
        """ Using memory private object elements is walked. 
        If an older element exists, incremental are created and added to
            elements 
        eoc: only is saved in memory
        """

        #TODO:
        # COMPROBAR QUE self.__memory ESTÁ GUARDANDO BIEN
        # LAS CLAVES DEL SWITCH AL QUE SE PREGUNTA

        new_elements = {}
        elements_to_del = []
        
        for key in elements:

            if self.__memory.exist(key):
                # add datediff field
                self.add_datediff(elements, key)

                # the element register exists
                elements_to_add = {}

                for metric in elements[key]:
                    # make incremental fields management
                    if metric in incremental_fields:
                        new_value = elements[key][metric]
                        new_ts = elements[key]['logTimestamp']
                        (old_value, old_ts) = self.__memory.get_instance(key, metric)
                        new_values = self.get_incrementals( metric, new_value,
                            old_value, new_ts,  old_ts)
                        for new_value in new_values:
                            if new_values.has_key(new_value) and new_values[new_value]:
                                elements_to_add[new_value] = new_values[new_value]
                    
                    # update elements[key] dictioanry
                    element = elements[key]

                # check if is possible calculate bandwith,
                # it will depend of the fields available
                # first we create a new dictionary with key filds in elements
                all_fields = elements[key].copy()
                # add to the elements from the temporal elements to add the 
                # incremental new elements calculated
                all_fields.update(elements_to_add)

                if self.__bandwidth_fields_set.issubset(set(all_fields.keys())):

                    seconds = all_fields['DeltaTime']
                    speed = int(all_fields['Speed'])
                    increment_in_octets = all_fields['InOctetsDiff']
                    increment_out_octets = all_fields['OutOctetsDiff']
                    
                    try:
                        elements_to_add['Bandwidth'] \
                            = self.bandwidth_calculation(seconds, 
                                                       speed, 
                                                       increment_in_octets,
                                                       increment_out_octets)
                    except ValueError as e:
                        logging.error("Error calculating bandwith for %s: %s" %( key, repr(e)))
                    
                elements[key].update(elements_to_add)

            else:                
                elements_to_del.append(key)
            
            # update memory
            self.__memory.set_instance(key, elements[key])

            
        for key in elements_to_del:
            del elements[key]

    def bandwidth_calculation(self, seconds, speed, increment_in_octets,
        increment_out_octets):
        """ Bandwidtch is the average of utilization for a full duplex network
        interface. The formula:

            >>> max (Delta_in_octest, Delta_out_octets) * 8 / 
                ( seconds * speed)

        Ref: http://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/8141-calculate-bandwidth-snmp.html
        """
        if seconds <= 0 :
            logging.debug("seconds value less than 0: %s" %seconds)
            raise ValueError("seconds value must be greater than 0")
        elif speed <= 0:
            logging.debug("speed value less than 0: %s" %speed)
            raise ValueError("speed value must be greater than 0")

        result = ( max (increment_out_octets,increment_in_octets) * 8 ) / \
                ( seconds * speed)

        if result > 1:
            logging.critical(" bandwidth > 1, formula of bandwidth:   max(%s, %s) * 8 * 100 /  (%s * %s) = %s"
                %(increment_in_octets, increment_out_octets, seconds, speed, result))

        return result

    def get_incrementals(self, metric_name, new_value, old_value, new_ts, old_ts, 
        register_bytes=32):

        max_value = pow(2, register_bytes) -1 

        new_ammount = int(re.findall(r'\d+',new_value)[0])
        old_ammount = int(re.findall(r'\d+',old_value)[0])
        
        result = {}        
        
        if old_ammount > max_value:
            logging.critical("old_ammount of %s is greater than max (%s): %s"
                %(metric_name, max_value, old_ammount))
        elif new_ammount > max_value:
            logging.critical("new_ammount of %s is greater than max (%s): %s"
                %(metric_name, max_value, new_ammount))
        else:

            if new_ammount < old_ammount:
                new_ammount += pow(2,register_bytes) - 1

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

    def __apply_map(self, data):

        for element_k in data:
            for map_k in self.__mapping.keys():
                if data[element_k].has_key(map_k):
                    data[element_k][map_k] = self.__mapping[map_k](data[element_k][map_k])

    def __add_custom_fields(self, elements, custom_data):
        for item in elements:
            for field in custom_data:
                elements[item][field] = custom_data[field]
                #logging.debug('added custom field %s => %s to data' %(field, custom_data[field]))

    def run(self):

        while not self.stop_event.is_set():
            try:
                product = self.input_queue.get(True, 1)
                
                (elements, incremental_fields, custom_data) = product

                if self.__mapping:
                    self.__apply_map(elements)

                # calculate incremental fields
                if incremental_fields:
                    self.do_increments(elements, incremental_fields)

                # add custom data to elements, you know, fields from
                # config file to add to each data
                if custom_data:
                    self.__add_custom_fields(elements, custom_data)

                if elements:
                    logging.debug('***** adding elements to send_queue')
                    self.send_queue.put(elements)

            except Empty:
                pass


class SenderThread(Thread):

    def __init__( self, queue, cfg=None, name=None):

        super(SenderThread, self).__init__(name=name)

        if not queue:
            raise ValueError('queue parameter cannot be null')

        if type(cfg) == list and ( len(cfg) != 2 or \
            type(cfg[0]) != str or type(cfg[1]) != int ):
            raise ValueError('cfg parameter must be list with len 2 ')

        if cfg:
            self.server = cfg[0]
            self.port = cfg[1]
        else:
            self.server = '127.0.0.1'
            self.port = 8000

        self.input_queue = queue
        self.stop_event = Event()


    def stop(self):
        self.stop_event.set()


    def send_message(self, message):
        
        while True:
            try:
                sock = socket.socket(socket.AF_INET, # Internet
                                     socket.SOCK_DGRAM) # UDP
            except socket.error, err:
                time_sleep(1)
                logging.error("Error sending data: %s" %repr(err))
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
                message = self.input_queue.get(True, 1)
                logging.info('thread read data from sender queue')
                self.send_message(message)
            except Empty as exception:
                pass
            else:
                logging.critical(" sent message %s... to %s" 
                    %(str(message)[0:30], self.server))

