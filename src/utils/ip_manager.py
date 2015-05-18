#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_decimal_ip(hexadecimal_ip):
        decimal_ip_array = [ str(int('0x'+hex,0)) for hex in hexadecimal_ip.split(' ')]
        return '.'.join(decimal_ip_array)