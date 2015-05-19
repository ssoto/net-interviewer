#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import pytz
import re
import subprocess

class Snmp_table_request:
    """
    Example of how could be a generic snmp table request

    options are 

    """
    def __init__ (self, server, port=161, community="public", snmp_version="2c", mib_name=None, oid_name=None, cmd_options=None):
        
        default_arguments = "-Cf", ",", "-Cl", "-CB", "-Ci", "-OX", "-Cb", "-Oe"
        
        self.server = server
        self.port = port
        self.community = community
        self.snmp_version = snmp_version
        self.mib_name = mib_name
        self.oid_name = oid_name
        logging.debug("created new ")
        self.__cmd = ["snmptable",
                     "-v",
                     snmp_version,
                     "-c",
                     community, 
                     server]

        self.__cmd.extend(default_arguments)

        self.__cmd.append(mib_name + ":" + oid_name)


    def __get_current_time(self):

        utc = pytz.utc
        fmt = '%Y-%m-%d %H:%M:%S %Z'
        madrid_tz = pytz.timezone('Europe/Madrid')

        dt = datetime.datetime.now()
        madrid_dt = madrid_tz.localize(dt)
        return madrid_dt.astimezone(utc).strftime(fmt)


    def request(self, simulate=False):
        #TODO: make a real subprocess.checkoutput(cmd)
        #
        if simulate:
            if self.oid_name == 'cDot11ClientConfigInfoTable' and self.mib_name == 'CISCO-DOT11-ASSOCIATION-MIB':
                self.raw_output = """index,ParentAddress,RoleClassType,DevType,RadioType,WepEnabled,WepKeyMixEnabled,MicEnabled,PowerSaveMode,Aid,DataRateSet,SoftwareVersion,Name,AssociationState,IpAddressType,IpAddress,VlanId,SubIfIndex,AuthenAlgorithm,AdditionalAuthen,Dot1xAuthenAlgorithm,KeyManagement,UnicastCipher,MulticastCipher,DevObjectID,NewKeyManagement\n[1]["WellnessTelecom"][c4:93:0:1:eb:61],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,12,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 6B ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 """""
            elif self.oid_name == 'cDot11ClientStatisticTable' and self.mib_name == 'CISCO-DOT11-ASSOCIATION-MIB':
                self.raw_output = """index,CurrentTxRateSet,UpTime,SignalStrength,SigQuality\n[1]["WTInvitados"][0:21:6a:65:ec:aa],"06 ",4856 second,-49 dBm,48 percentage\n[1]["WellnessTelecom"][0:24:d7:56:22:64]," ",23025 second,-72 dBm,25 percentage\n[1]["WellnessTelecom"][4:46:65:ce:99:be],"04 ",11564 second,-54 dBm,41 percentage\n[1]["WellnessTelecom"][c:60:76:7:c9:73]," ",21815 second,-59 dBm,37 percentage\n[1]["WellnessTelecom"][14:b4:84:5e:d8:51],"07 ",2796 second,-60 dBm,37 percentage\n[1]["WellnessTelecom"][18:cf:5e:cf:3a:9d],"02 ",15295 second,-38 dBm,55 percentage\n[1]["WellnessTelecom"][1c:65:9d:74:41:c6],"07 ",18474 second,-42 dBm,54 percentage\n[1]["WellnessTelecom"][1c:65:9d:e5:65:c2],"01 ",20921 second,-48 dBm,48 percentage\n[1]["WellnessTelecom"][2c:d0:5a:8d:bf:b],"03 ",4156 second,-57 dBm,40 percentage\n[1]["WellnessTelecom"][2c:d0:5a:8d:bf:a1],"07 ",18336 second,-48 dBm,48 percentage\n[1]["WellnessTelecom"][2c:d0:5a:8d:cd:d6],"01 ",20693 second,-65 dBm,30 percentage\n[1]["WellnessTelecom"][38:b:40:de:42:23],"07 ",3132 second,-53 dBm,43 percentage\n[1]["WellnessTelecom"][38:b:40:de:42:a1],"03 ",173 second,-62 dBm,35 percentage\n[1]["WellnessTelecom"][38:94:96:29:19:e],"04 ",10942 second,-43 dBm,54 percentage\n[1]["WellnessTelecom"][40:e:85:58:e0:e3],"02 ",19266 second,-63 dBm,34 percentage\n[1]["WellnessTelecom"][40:f0:2f:a5:32:dc],"06 ",7340 second,-50 dBm,44 percentage\n[1]["WellnessTelecom"][40:f0:2f:a5:48:47],"04 ",3229 second,-63 dBm,34 percentage\n[1]["WellnessTelecom"][40:f0:2f:a5:48:8d],"03 ",21384 second,-54 dBm,41 percentage\n[1]["WellnessTelecom"][40:f0:2f:a5:49:73],"05 ",4086 second,-49 dBm,46 percentage\n[1]["WellnessTelecom"][40:f0:2f:a5:4d:9a],"05 ",8428 second,-45 dBm,47 percentage\n[1]["WellnessTelecom"][40:f0:2f:a5:4d:ce],"02 ",22775 second,-63 dBm,32 percentage\n[1]["WellnessTelecom"][40:f0:2f:a5:52:b],"03 ",6772 second,-51 dBm,44 percentage\n[1]["WellnessTelecom"][40:f0:2f:a5:64:9f],"04 ",13616 second,-50 dBm,47 percentage\n[1]["WellnessTelecom"][40:f0:2f:a5:68:15],"03 ",19227 second,-66 dBm,29 percentage\n[1]["WellnessTelecom"][4c:80:93:90:f0:fb],"07 ",18923 second,-56 dBm,40 percentage\n[1]["WellnessTelecom"][54:27:1e:8:d3:c2],"01 ",3141 second,-51 dBm,42 percentage\n[1]["WellnessTelecom"][60:21:c0:ca:e:f4],"07 ",751 second,-57 dBm,33 percentage\n[1]["WellnessTelecom"][68:a3:c4:9:4b:5d],"03 ",21234 second,-45 dBm,52 percentage\n[1]["WellnessTelecom"][7c:c5:37:3a:ef:e7],"05 ",1699 second,-56 dBm,39 percentage\n[1]["WellnessTelecom"][80:57:19:f1:49:9e],"07 ",10625 second,-48 dBm,47 percentage\n[1]["WellnessTelecom"][88:63:df:78:51:6e],"04 ",276 second,-77 dBm,20 percentage\n[1]["WellnessTelecom"][b4:3a:28:5c:0:12],"07 ",412 second,-52 dBm,44 percentage\n[1]["WellnessTelecom"][c4:62:ea:6a:1d:8a],"05 ",1651 second,-65 dBm,25 percentage\n[1]["WellnessTelecom"][c4:93:0:1:eb:61],"06 ",87982 second,-61 dBm,26 percentage\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],"04 ",85954 second,-68 dBm,29 percentage\n[1]["WellnessTelecom"][d8:fc:93:11:be:e9],"08 ",11963 second,-65 dBm,32 percentage\n[1]["WellnessTelecom"][d8:fc:93:11:be:ee],"01 ",20242 second,-68 dBm,28 percentage\n[2]["WellnessTelecom"][0:24:d7:67:e3:48],"0F ",13213 second,-54 dBm,33 percentage\n[2]["WellnessTelecom"][0:24:d7:7f:62:34],"0F ",19205 second,-57 dBm,30 percentage\n[2]["WellnessTelecom"][0:24:d7:7f:fe:bc],"0F ",14867 second,-56 dBm,31 percentage\n[2]["WellnessTelecom"][0:24:d7:80:50:8c],"07 ",20025 second,-52 dBm,36 percentage\n[2]["WellnessTelecom"][0:24:d7:ad:a8:84],"0F ",12468 second,-59 dBm,35 percentage\n[2]["WellnessTelecom"][1c:1a:c0:1e:3a:ff],"07 ",39 second,-76 dBm,19 percentage\n[2]["WellnessTelecom"][38:b:40:de:40:f5],"06 ",11515 second,-59 dBm,36 percentage\n[2]["WellnessTelecom"][38:b:40:de:41:3b],"07 ",4168 second,-47 dBm,49 percentage\n[2]["WellnessTelecom"][80:57:19:f1:49:72],"07 ",4101 second,-49 dBm,45 percentage\n[2]["WellnessTelecom"][a0:88:b4:2e:de:1c],"06 ",16546 second,-70 dBm,18 percentage\n[2]["WellnessTelecom"][b4:3a:28:5b:ff:f4],"07 ",8797 second,-59 dBm,36 percentage\n[2]["WellnessTelecom"][b4:3a:28:5c:0:24],"07 ",12340 second,-58 dBm,37 percentage\n[2]["WellnessTelecom"][b4:b6:76:86:c6:b2],"07 ",406 second,-51 dBm,43 percentage\n[2]["WellnessTelecom"][c0:ee:fb:26:2d:ae],"04 ",4107 second,-51 dBm,44 percentage\n[2]["WellnessTelecom"][c4:50:6:78:a3:9b],"07 ",4171 second,-52 dBm,44 percentage\n[2]["WellnessTelecom"][d8:fc:93:11:4b:58],"0F ",2338 second,-58 dBm,29 percentage\n[2]["WellnessTelecom"][d8:fc:93:11:b5:4d],"05 ",3408 second,-60 dBm,33 percentage\n[2]["WellnessTelecom"][e0:b5:2d:2:d8:5f],"07 ",1650 second,-50 dBm,45 percentage"""
        else:
            self.__timestamp = self.__get_current_time()
            logging.debug('timestamp local: %s' % self.__timestamp)
            try:
                self.raw_output = subprocess.check_output(self.__cmd)
            except Exception as call_error:
                logging.error("Error doing request")
                raise

    def get_json_reply(self):
        if hasattr(self, 'json_output'):
            return self.json_output
        elif not hasattr(self, 'raw_output'):
            raise AttributeError('request output has not been established... Request has not been done or failed')
        else:
            tmp_list = [ x.split(',') for x in self.raw_output.split('\n') ]
            # delete first 2 lines, an inroduccion message for the MIB
            output_list = tmp_list[2:]
            
            header = output_list[0]
            rows = output_list[1:-1]

            self.json_output = self._get_body_dict(header, rows)

            return self.json_output

    def _get_body_dict(self, header, elements):

        result = {}

        num_rows = len(elements)
        num_colums = len(header)
        
        prog = re.compile( r"\[([a-zA-Z0-9_:]+)\]\[([a-zA-Z0-9_:]+)\]\[([a-zA-Z0-9_:]+)\]")
        
        for i in range(0, num_rows):
            element_dict = {}
            for j in range(0, num_colums):
                element_dict[header[j]] = (elements[i][j]).translate(None, '"').strip()
            m = prog.match(element_dict['index'])

            (num_id, ssid, mac_address) = m.groups()
            element_dict['MacAddress'] = mac_address
            element_dict['SSIDName'] = ssid
            element_dict['logTimestamp'] = self.__timestamp

            #manage dictionary key. I'm going to use the MAC to search after
            result[mac_address] = element_dict
        return result
