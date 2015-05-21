#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import re
import socket

class Sender():

    def __init__(self, server, port):
        self.__ip = server
        self.__port = port
        self.__memory_dict = None

    def send_dict_values(self, dict_2_send, register_fields=None):

        if register_fields and len(register_fields):
                        
            original = dict_2_send

            if self.__memory_dict:
                final_dict = self.__update_registers_fields(dict_2_send, register_fields)
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

    def __update_registers_fields(self, dictionary, fields):
        # mac identifier level
        for element_key in dictionary:

            # I get only values for fields list
            new_values = {k: v for k, v in dictionary[element_key].items() if k in fields}
            try:
                old_values = {k: v for k, v in (self.__memory_dict[element_key]).items() if k in fields}
            except KeyError as e:
                logging.info("New device: " + element_key)
                break
            for field in fields:
                if new_values[field] and old_values[field]:
                    new_ammount = int(re.findall(r'\d+',new_values[field])[0])
                    old_ammount = int(re.findall(r'\d+',old_values[field])[0])

                    dictionary[element_key][field+'Diff'] = abs(old_ammount - new_ammount)
                else:
                    pass
            #import ipdb; ipdb.set_trace()
        return dictionary
            
        
if __name__ == "__main__":
    obj = {
        "14:30:c6:bb:ef:14": {
            "index": "[1][WellnessTelecom][14:30:c6:bb:ef:14]", 
            "UpTime": "14251 second", 
            "IpAddress": "10.200.3.112", 
            "AgingLeft": "50 second", 
            "SignalStrength": "-54 dBm", 
            "Duplicates": "3 packet", 
            "MsduFails": "0 packet", 
            "BytesReceived": "1327199 byte", 
            "CurrentTxRateSet": "07", 
            "PacketsReceived": "8155 packet", 
            "MacAddress": "14:30:c6:bb:ef:14", 
            "BytesSent": "3126874 byte", 
            "MicMissingFrames": "0 packet", 
            "SigQuality": "42 percentage", 
            "MicErrors": "0 error", 
            "PacketsSent": "5174 packet", 
            "WepErrors": "0 packet", 
            "MsduRetries": "1940 packet"
        },
        "80:57:19:f1:49:7c": {
            "index": "[2][WellnessTelecom][80:57:19:f1:49:7c]", 
            "UpTime": "18176 second", 
            "IpAddress": "10.200.3.149", 
            "AgingLeft": "56 second", 
            "SignalStrength": "-51 dBm", 
            "Duplicates": "33 packet", 
            "MsduFails": "0 packet", 
            "BytesReceived": "4287318 byte", 
            "CurrentTxRateSet": "07", 
            "PacketsReceived": "32752 packet", 
            "MacAddress": "80:57:19:f1:49:7c", 
            "BytesSent": "19326816 byte", 
            "MicMissingFrames": "0 packet", 
            "SigQuality": "48 percentage", 
            "MicErrors": "0 error", 
            "PacketsSent": "29229 packet", 
            "WepErrors": "0 packet", 
            "MsduRetries": "1097 packet"
        }
    }

    s = Sender('127.0.0.1', 8000)
    s.send_dict(obj)