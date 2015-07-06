#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Queue import Queue
import unittest2
import datetime

from interviewer.utils.threads import Memory


import logging
logging.basicConfig( format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
                     level=logging.DEBUG)

class TestReaderMemoryClass(unittest2.TestCase):

    def setUp(self):

        self.m = Memory()

    def tearDown(self):
        self.m = None

    def test_get_intsance_1(self):
        """ Memory.set_instance: returns the metric assigned right before """

        now_timestamp =  str(datetime.datetime.now())
        key = '00:90:f5:f5:42:c5'
        value = { 'metric1':23, 
                  'metric2':'FasEthernet',
                  'logTimestamp': now_timestamp}

        self.m.set_instance( key, value)

        self.assertEqual(self.m.get_instance(key, 'metric1'), 
                         (23, now_timestamp))

    def test_get_intsance_2(self):
        """ Memory.set_instance: update an already existent metric value """

        now_timestamp =  str(datetime.datetime.now())
        key = '00:90:f5:f5:42:c5'
        value = { 'metric1':23, 
                  'metric2':'FasEthernet',
                  'logTimestamp': now_timestamp }

        self.m.set_instance(key, value)

        #alter the value of metric1
        value['metric1'] = 0

        self.m.set_instance( key, value )

        self.assertEqual(self.m.get_instance(key, 'metric1'), 
                         (0, now_timestamp))        

    def test_exist_1(self):
        """ Memory.exist: element not inserted doesn't exist"""
        self.assertEqual(self.m.exist('00:90:f5:f5:42:c5'), False)

    def test_exist_2(self):
        """ Memory.exist: element not inserted doesn't exist"""
        
        self.assertEqual(self.m.exist('00:90:f5:f5:42:c5'), False)

    def test_get_timestamp_1(self):
        """Testing get_timestamp with entry"""
        now_timestamp =  str(datetime.datetime.now())
        key = '00:90:f5:f5:42:c5'
        value = { 'metric1':23, 
                  'metric2':'FasEthernet',
                  'logTimestamp': now_timestamp}

        self.m.set_instance( key, value)
        self.assertEqual(self.m.get_timestamp(key) == now_timestamp, True)

    def test_get_timestamp_2(self):
        """Testing get_timestamp with non existing key"""
        key = '00:90:f5:f5:42:c5'

        with self.assertRaises(KeyError):
            self.m.get_timestamp(key)