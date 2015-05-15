#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import pprint

class Snmp_table_request:
    """
    Example of how could be a generic snmp table request

    options are 

    """
    def __init__ (self, server, port, community, snmp_version, mib_name, oid_name, cmd_options=None):
        default_arguments = "-Cf", ",", "-Cl", "-Ch", "-CB", "-Ci", "-OX", "-Cb", "-Oe"
        self._cmd = ["snmptable", 
                     community, 
                     "-c" + community, 
                     "10.200.0.10",
                     default_arguments, 
                    mib_name + ":" + oid_name]

    def request(self):

        #TODO: make a real subprocess.checkoutput(cmd)
        output = """index,ParentAddress,RoleClassType,DevType,RadioType,WepEnabled,WepKeyMixEnabled,MicEnabled,PowerSaveMode,Aid,DataRateSet,SoftwareVersion,Name,AssociationState,IpAddressType,IpAddress,VlanId,SubIfIndex,AuthenAlgorithm,AdditionalAuthen,Dot1xAuthenAlgorithm,KeyManagement,UnicastCipher,MulticastCipher,DevObjectID,NewKeyManagement\n[1]["WellnessTelecom"][c4:93:0:1:eb:61],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,12,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 6B ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 "\n[1]["WellnessTelecom"][c4:93:0:1:eb:85],0:23:4:c9:d6:70,-1,1,1,1,2,2,1,13,"02 04 0B 0C 12 16 18 24 30 48 60 6C ",.,.,3,1,"0A C8 03 66 ",300,9,1,"40 ","20 ","00 ","04 ","04 ",SNMPv2-SMI::zeroDotZero,"20 """""

        output_list = [ x.split(",") for x in output.split("\n") ]
        # optimization stuff: len(header) is been only calculated onece
        self.num_rows = len(output_list[0])
        header = output_list[0]
        result = self._process_body(header, output_list[1:])
        return result

    def _process_body(self, header, elements):
        #import pdb; pdb.set_trace() #BREAKPOINT 
        result = {}
        num_elements = len(elements)
        for elements_index in range(0, num_elements):
            element_dict = {}
            for index in range(0, self.num_rows): 
                element_dict[header[index]] = (elements[elements_index][index]).translate(None, '"')
            result[elements_index] = element_dict
        return result


def do():
    table_req = Snmp_table_request("10.200.0.10", 
                                   "wtelecom", 
                                   "2c",
                                   161,
                                   "CISCO-DOT11-ASSOCIATION-MIB", 
                                   "cDot11ClientConfigInfoTable")
    result = table_req.request()
    #print pprint.pprint(result)

def do_times(times=1000):
    for i in range(0,times):
        do()

if __name__ == "__main__":
    import cProfile
    # 1000000 times: 31.298 seconds
    cProfile.runctx('do_times(10000)', None, locals())
    