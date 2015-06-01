#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import re
import socket

from utils.timeutils import times_str_diff

class Sender():

    def __init__(self, server, port):
        self.__ip = server
        self.__port = port


    def iterate_and_send(self, dict_2_send):

        for element in dict_2_send:
            dict_str = json.dumps(dict_2_send[element])
            sock = socket.socket(socket.AF_INET, # Internet
                                 socket.SOCK_DGRAM) # UDP
            sock.sendto(dict_str, 
                        (self.__ip, self.__port))