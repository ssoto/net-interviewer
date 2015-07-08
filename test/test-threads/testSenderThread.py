#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Queue import Queue
import unittest2

from interviewer.utils.threads import SenderThread
import logging
# logging.basicConfig( format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
#                      level=logging.DEBUG)

class TestReaderSenderThread(unittest2.TestCase):

    def setUp(self):
        self.q = Queue()
        self.cfg = ['10.128.19.10', 4000]
        self.name = 'SenderTester'


    def tearDown(self):
        self.s_th = None
        self.q = None
        self.name = None

    def test_cfg_input_1(self):
        """SenderThread(): cfg input parameter empty list raise ValueError"""
        cfg = []
        with self.assertRaises(ValueError):
            s = SenderThread(self.q, cfg, self.name)


    def test_cfg_input_2(self):
        """SenderThread(): incorrect first element of cfg parameter must raise ValueError"""
        cfg = [1000, 8000]
        with self.assertRaises(ValueError):
            s = SenderThread(self.q, cfg, self.name)

    def test_cfg_input_3(self):
        """SenderThread(): incorrect second element of cfg parameter must raise ValueError"""
        cfg = ['127.0.0.1', '8000']
        with self.assertRaises(ValueError):
            s = SenderThread(self.q, cfg, self.name)

    def test_queue_input_1(self):
        """SenderTrhead(): incorrect Queue input parameter must raise ValueError"""
        q = None
        with self.assertRaises(ValueError):
            SenderThread(q, self.cfg, self.name)



