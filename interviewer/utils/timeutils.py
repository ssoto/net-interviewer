#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging

def get_date_format():
    return '%Y-%m-%d %H:%M:%S'

def get_current_time(date_format_str=None):
    if not date_format_str:
        date_format_str = get_date_format()

    utc_now = datetime.datetime.utcnow()
    now = datetime.datetime.now()
    return now.strftime(get_date_format())

def parse_datetime(date_str, date_format_str=None):
    if not date_format_str:
        date_format_str = get_date_format()
    return datetime.datetime.strptime(date_str, date_format_str)


def times_str_diff( first_time_str, second_time_str):

    date_1 = parse_datetime(first_time_str)
    date_2 = parse_datetime(second_time_str)

    # check which date is bigger
    if date_1 > date_2:
        return (date_1 - date_2).total_seconds()        
    else:
        return (date_2 - date_1).total_seconds()
