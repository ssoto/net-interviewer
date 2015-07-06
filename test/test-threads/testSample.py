#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Queue import Queue
from unittest import TestCase
from mock import MagicMock
import datetime


import logging
logging.basicConfig( format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
                     level=logging.DEBUG)

class TestSampleClass(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

