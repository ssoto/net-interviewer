#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_decimal_ip(hexadecimal_ip):
    """
    Parse snmptable output ip in hexadecimal extrange format and return a 
    common ip:
    >>>> ip = '0A C8 03 47'
    >>>> print get_decimal_ip(ip)
    10.200.3.71

    """
    decimal_ip_array = [ str(int('0x'+hex,0)) for hex in hexadecimal_ip.strip().split(' ')]
    return '.'.join(decimal_ip_array)
