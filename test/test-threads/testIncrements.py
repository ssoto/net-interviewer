#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
import datetime
from Queue import Queue

from interviewer.utils.threads import ReaderThread, Memory


class TestSampleClass(unittest.TestCase):

    def setUp(self):
        self.m = Memory()
        self.raw_q = Queue()
        self.send_q = Queue()
        self.r_th = ReaderThread(self.raw_q, self.send_q, 'TestThread', self.m)


    def tearDown(self):
        self.r_th.stop()
        self.r_th = None


    @mock.patch('interviewer.utils.threads.Memory')
    @mock.patch('Queue.Queue')
    def test_creation(self, MockMemory, MockQueue):
        m = MockMemory()
        raw_q = MockQueue()
        send_q = MockQueue()
        r_th = ReaderThread(raw_q, send_q, 'TestThread', m)


    def test_first_call(self):
        """ REaderThread.do_increments() TODO"""
        self.r_th.start()

        data1 = {'[2]["WellnessTelecom"][d8:fc:93:11:d2:4e]': {'AgingLeft': '50 second',
                                               'AssociationState': '3',
                                               'BytesReceived': '21803026 byte',
                                               'BytesSent': '46846873 byte',
                                               'CurrentTxRateSet': '0F ',
                                               'Duplicates': '1 packet',
                                               'IpAddress': '0A C8 03 3A ',
                                               'MicErrors': '0 error',
                                               'MicMissingFrames': '0 packet',
                                               'MsduFails': '0 packet',
                                               'MsduRetries': '5249 packet',
                                               'PacketsReceived': '83326 packet',
                                               'PacketsSent': '73255 packet',
                                               'ParentAddress': '0:23:4:78:b3:60',
                                               'SigQuality': '36 percentage',
                                               'SignalStrength': '-52 dBm',
                                               'UpTime': '21570 second',
                                               'VlanId': '300',
                                               'WepErrors': '0 packet',
                                               'index': '[2]["WellnessTelecom"][d8:fc:93:11:d2:4e]',
                                               'logTimestamp': '2015-07-03 14:21:18'}}
        data2 = {'[2]["WellnessTelecom"][d8:fc:93:11:d2:4e]': {'AgingLeft': '50 second',
                                               'AssociationState': '3',
                                               # data 1 + 300
                                               #'BytesReceived': '21803026 byte',
                                               'BytesReceived': '21803326 byte',
                                               # data 1 + 300
                                               #'BytesSent': '46846873 byte',
                                               'BytesSent': '46847173 byte',
                                               'CurrentTxRateSet': '0F ',
                                               'Duplicates': '1 packet',
                                               'IpAddress': '0A C8 03 3A ',
                                               'MicErrors': '0 error',
                                               'MicMissingFrames': '0 packet',
                                               'MsduFails': '0 packet',
                                               'MsduRetries': '5249 packet',
                                               # data 1 + 100
                                               #'PacketsReceived': '83326 packet',
                                               'PacketsReceived': '83626 packet',
                                               # data 1 + 100
                                               #'PacketsSent': '73255 packet',
                                               'PacketsSent': '73555 packet',
                                               'ParentAddress': '0:23:4:78:b3:60',
                                               'SigQuality': '36 percentage',
                                               'SignalStrength': '-52 dBm',
                                               'UpTime': '21570 second',
                                               'VlanId': '300',
                                               'WepErrors': '0 packet',
                                               'index': '[2]["WellnessTelecom"][d8:fc:93:11:d2:4e]',
                                               'logTimestamp': '2015-07-03 14:21:18'}}
        incremental_fields = ['PacketsSent', 'PacketsReceived', 'BytesSent', 'BytesReceived']

        custom_fields = {}
        custom_fields['DeviceId'] = 'WT_ap_1'

        self.raw_q.put((data1, incremental_fields, custom_fields))

        self.raw_q.put((data2, incremental_fields, custom_fields))


    def get_incrementals_1(self, )

        




if __name__ == '__main__':
    unittest.main()
