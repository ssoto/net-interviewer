#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import re
import socket

from utils.time import times_str_diff

class Sender():

    def __init__(self, server, port):
        self.__ip = server
        self.__port = port
        self.__memory_dict = None

    def send_dict_values(self, dict_2_send, register_fields=None, timestamp_field='logTimestamp'):

        if register_fields and len(register_fields):
            
            original = dict_2_send

            if self.__memory_dict:
                final_dict = self.__update_registers_fields( dict_2_send, 
                                                             register_fields, 
                                                             timestamp_field)
                self.__iterate_and_send(final_dict)
            
            self.__memory_dict = original
        else:
            # dict "sotred" is the original, without managing register fields
            self.__iterate_and_send(dict_2_send)

    def __iterate_and_send(self, dict_2_send):

        for element in dict_2_send:
            dict_str = json.dumps(dict_2_send[element])
            sock = socket.socket(socket.AF_INET, # Internet
                                 socket.SOCK_DGRAM) # UDP
            sock.sendto(dict_str, 
                        (self.__ip, self.__port))

    def __update_registers_fields(self, dictionary, fields, timestamp_field):
        # mac identifier level
        for element_key in dictionary:

            # get only values for fields list
            new_values = {k: v for k, v in dictionary[element_key].items() if k in fields}
            try:
                old_values = {k: v for k, v in (self.__memory_dict[element_key]).items() if k in fields}
            except KeyError as e:
                logging.info("New device: " + element_key)
                break
            for field in fields:
                if new_values[field] and old_values[field]:
                    try:
                        new_ammount = int(re.findall(r'\d+',new_values[field])[0])
                        old_ammount = int(re.findall(r'\d+',old_values[field])[0])
                    except IndexError as e:
                        #logging.error("error parsing field " + field + ":\n" + repr(e))
                        pass

                    key_diff = abs(old_ammount - new_ammount)
                    dictionary[element_key][field+'Diff'] = key_diff

                    try:
                        time_diff = times_str_diff(dictionary[element_key][timestamp_field],
                                                               self.__memory_dict[element_key][timestamp_field])
                        key_diff_rate = key_diff / time_diff

                        dictionary[element_key][field+'DiffRate'] = key_diff_rate 
                        dictionary[element_key]['DeltaTime'] = time_diff
                    except ZeroDivisionError as ex:
                        logging.debug("ZeroDivisionError in field field: " %(field))
                        pass

                    # logging.debug(  field + "Diff  => " + str(key_diff))
                    # logging.debug(  field + "DiffRate  => " + str(key_diff_rate))

                else:
                    pass
        return dictionary
