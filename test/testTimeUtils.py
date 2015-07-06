#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
import datetime
from Queue import Queue

from interviewer.utils.timeutils import get_current_time, parse_datetime, times_str_diff


class TestCurrentDateTimeFunction(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_current(self):
        """test_current(): returns a string"""

        current_ts = get_current_time()

        self.assertTrue(type(current_ts) == str)


class TestDatetimeDiffClass(unittest.TestCase):

    def setUp(self):
        self.a_dt = "2015-06-01 11:15:53"
        self.b_dt = "2015-06-02 11:15:53"

    def test_dateDiff_1(self):
        """times_str_diff(ts1, ts2): 1 day difference """

        
        self.assertEqual(times_str_diff(self.a_dt, self.b_dt), 1*24*60*60)

    def test_dateDiff_2(self):
        """times_str_diff(dt2, dt1): 1 day difference with bigger first"""


        self.assertEqual(times_str_diff(self.b_dt,self.a_dt), 1*24*60*60)

    def test_dateDiff_3(self):
        """times_str_diff(dt2, dt1): assert if the same date, difference is 0"""

        self.assertEqual(times_str_diff(self.a_dt, self.a_dt), 0*24*60*60)


class TesDateTimeClass(unittest.TestCase):

    def setUp(self):
        self.a_ts = "2015-06-01 11:15:53"


    def tearDown(self):
        pass

    def test_parse_date_year(self):
        """parse_datetime(dt): year componet of a proper datetime are fine after been parsed"""

        
        parsed_dt = parse_datetime(self.a_ts)
        self.assertEqual(parsed_dt.year, 2015)

    def test_parse_date_month(self):
        """parse_datetime(dt): month componet of a proper datetime are fine after been parsed"""

        parsed_dt = parse_datetime(self.a_ts)
        self.assertEqual(parsed_dt.month, 6)

    def test_parse_date_day(self):
        """parse_datetime(dt): day componet of a proper datetime are fine after been parsed"""

        parsed_dt = parse_datetime(self.a_ts)
        self.assertEqual(parsed_dt.day, 1)

    def test_parse_date_hour(self):
        """parse_datetime(dt): all componets of a proper datetime hour had been fine  parsed"""

        parsed_dt = parse_datetime(self.a_ts)
        self.assertEqual(parsed_dt.hour, 11)
        self.assertEqual(parsed_dt.minute, 15)
        self.assertEqual(parsed_dt.second, 53)
