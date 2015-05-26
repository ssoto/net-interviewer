#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_current_time(date_format_str=None):
    if not date_format_str:
        date_format_str = DATE_FORMAT

    utc_now = datetime.datetime.utcnow()
    return utc_now.strftime(DATE_FORMAT)

def parse_datetime(date_str, date_format_str=None):
    if not date_format_str:
        date_format_str = DATE_FORMAT
    return datetime.datetime.strptime(date_str, date_format_str)


def get_diff_between_str_times( first_time_str, second_time_str):

    date_1 = parse_datetime(first_time_str)
    date_2 = parse_datetime(second_time_str)

    # check which date is bigger
    if date_1 > date_2:
        return (date_1 - date_2).total_seconds()        
    else:
        return (date_2 - date_1).total_seconds()