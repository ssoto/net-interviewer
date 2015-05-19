#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import socket


class Sender():

    def __init__(self, server, port):
        self.__ip = server
        self.__port = port

    def send_dict(self, dict):
        self.send_str(json.dumps(dict))

    def send_str(self, json_str):
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.sendto(json_str, 
                    (self.__ip, self.__port))

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