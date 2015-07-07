#!/usr/bin/env python
# -*- coding: utf-8 -*-

# non integer divisions
from __future__ import division

import unittest
import mock
import datetime
from Queue import Queue


from interviewer.utils.threads import ReaderThread


class TestSampleClass(unittest.TestCase):

    def setUp(self):
        self.raw_q = Queue()
        self.send_q = Queue()
        self.r_th = ReaderThread(self.raw_q, self.send_q, 'TestThread')


    def tearDown(self):
        self.r_th.stop()
        self.r_th = None


    def testGetIncrementals_1(self):
        """ ReaderThread.get_incrementals() returns normal Diff value valueIncrement = 7 and timeIncrement = 30
        """

        name = 'devil_metric'
        # Δvalue = 3
        old_value = '1'
        new_value = '4'
        # Δs = 30
        old_ts = '2015-07-06 12:17:15'
        new_ts = '2015-07-06 12:17:45'
        # range is [0, 2³-1] 
        register_bytes = 3

        result = self.r_th.get_incrementals(metric_name=name, new_value=new_value, 
            old_value=old_value, new_ts=new_ts, old_ts=old_ts, 
            register_bytes=register_bytes)
        
        self.assertIsNotNone(result[name+'Diff'])
        self.assertEqual(result[name+'Diff'] == 3, True)
        self.assertEqual(result[name+'DiffRate'] == None, False)
        self.assertEqual(result[name+'DiffRate'] == 3/30, True)

    def testGetIncrementals_2(self):
        """ ReaderThread.get_incrementals() returns check behaviour with overflow valueIncrement = 3 and timeINcrement = 30
        """
        name = 'devil_metric'
        # value = 3
        old_value = '5'
        new_value = '1'
        # Δs = 30
        old_ts = '2015-07-06 12:17:15'
        new_ts = '2015-07-06 12:17:45'
        # range is [0, 2³-1] => [0, 7]
        register_bytes = 3

        result = self.r_th.get_incrementals(metric_name=name, new_value=new_value, old_value=old_value, new_ts=new_ts, old_ts=old_ts, register_bytes=register_bytes)
        
        self.assertEqual(result[name+'Diff'] == None, False)
        self.assertEqual(result[name+'Diff'] == 3, True)
        self.assertEqual(result[name+'DiffRate'] == None, False)
        self.assertEqual(result[name+'DiffRate'] == 3/30, True)


    def testGetIncrementals_3(self):
        """ ReaderThread.get_incrementals() when  time increment is 0, the new DiffRate value cant be calculated, None
        """
        name = 'devil_metric'
        #Δvalue = 3
        old_value = '5'
        new_value = '1'
        # Δs = 0
        single_ts = '2015-07-06 12:17:15'
        # range is [0, 2³-1] => [0, 7]
        register_bytes = 3

        result = self.r_th.get_incrementals(metric_name=name, new_value=new_value, 
            old_value=old_value, new_ts=single_ts, old_ts=single_ts, 
            register_bytes=register_bytes)

        self.assertEqual(result[name+'Diff'] == None, False)
        self.assertEqual(result[name+'Diff'] == 3, True)
                
        with self.assertRaises(KeyError):
            result[name+'DiffRate']


    def testGetIncrementals_4(self):
        """ ReaderThread.get_incrementals() when value is high than maximum supported by the counter, None is returned
        """
        name = 'devil_metric'
        register_bytes = 3
        #Δvalue doesn't matter
        # range is [0, 2³-1] => [0, 7]
        old_value = '5'
        # new value is double of register maximum
        new_value = str((pow(2, register_bytes) - 1 ) * 2)
        # Δs = 0
        old_ts = '2015-07-06 12:17:15'
        new_ts = '2015-07-06 12:47:15'

        result = self.r_th.get_incrementals(metric_name=name, new_value=new_value, 
            old_value=old_value, new_ts=new_ts, old_ts=old_ts, 
            register_bytes=register_bytes)

        self.assertEqual(result, dict())