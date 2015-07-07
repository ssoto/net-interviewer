#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Queue import Queue
import unittest2

from interviewer.utils.threads import ReaderThread
import logging
# logging.basicConfig( format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
#                      level=logging.DEBUG)

class TestReaderThreadBandwidth(unittest2.TestCase):

    def setUp(self):
        queue = Queue()
        send_queue = Queue()

        self.r_th = ReaderThread(queue, send_queue, 'name')


    def tearDown(self):
        self.r_th = None


    def test_creation_null_input_queue(self):
        """ReaderThread(): ensure input queue is not None"""
        queue = Queue()
        with self.assertRaises(TypeError):
            r_th = ReaderThread(None, queue, 'Name')

    def test_creation_null_output_queue(self):
        """ReaderThread(): ensure output queue is not None"""
        queue = Queue()
        with self.assertRaises(TypeError):
            r_th = ReaderThread(queue, None, 'Name')

    def test_creation_null_name(self):
        """ReaderThread(): ensure thread Name is not None"""
        queue1 = Queue()
        queue2 = Queue()
        with self.assertRaises(TypeError):
            r_th = ReaderThread(queue1, queue2, None)

    def test_zero_division_error(self):
        """  ReaderThread.bandwidth_calculation: ensure raies ValueError"""
        seconds = 0
        speed = 1000000
        increment_in_octets = 30
        increment_out_octets  = 50
        with self.assertRaises(ValueError):

            self.r_th.bandwidth_calculation(
                                seconds,
                                speed,
                                increment_in_octets,
                                increment_out_octets)

    def test_hundred_percent_in (self):
        """  ReaderThread.bandwidth_calculation: return 1 (100%) ussing full in incremental octects"""
        seconds = 30
        speed = 1000000
        increment_in_octets = seconds * speed / 8
        increment_out_octets  = 50

        result = self.r_th.bandwidth_calculation(
                            seconds,
                            speed,
                            increment_in_octets,
                            increment_out_octets)

        self.assertEqual( result==1 , True)

    def test_hundred_percent_out (self):
        """  ReaderThread.bandwidth_calculation: return 1 (100%) ussing full out incremental octects"""
        seconds = 30
        speed = 1000000
        increment_out_octets = seconds * speed / 8
        increment_in_octets  = 50

        result = self.r_th.bandwidth_calculation(
                            seconds,
                            speed,
                            increment_in_octets,
                            increment_out_octets)

        self.assertEqual( result==1 , True)

    def test_fifty_percent_out (self):
        """  ReaderThread.bandwidth_calculation: 50% for output octets"""
        seconds = 30
        speed = 1000000
        increment_in_octets = 3
        increment_out_octets  = 0.5 * seconds * speed / 8

        result = self.r_th.bandwidth_calculation(
                                seconds,
                                speed,
                                increment_in_octets,
                                increment_out_octets)

        self.assertEqual( result==0.5 , True)

    def test_fifty_percent_in (self):
        """  ReaderThread.bandwidth_calculation: 50% for input octets """
        seconds = 30
        speed = 1000000
        increment_out_octets = 3
        increment_in_octets  = 0.5 * seconds * speed / 8

        result = self.r_th.bandwidth_calculation(
                                seconds,
                                speed,
                                increment_in_octets,
                                increment_out_octets)

        self.assertEqual( result==0.5 , True)


