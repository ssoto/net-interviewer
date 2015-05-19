#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_decimal_ip(hexadecimal_ip):
        decimal_ip_array = [ str(int('0x'+hex,0)) for hex in hexadecimal_ip.split(' ')]
        return '.'.join(decimal_ip_array)

def append_field(data, original_ds, destination_ds, field):
    """
    Try add a new field on destination_ds for each element in 
    destination_ds with same key. 

    >>> print data
    data  = {
        original_ds : {
            key_a : {
                target_field: value
                ...
            }
        },
        destination_ds : {
            key_a : {
                ...
            }
        } 
    }
    >>> append_field (data, "original_ds", "destination_ds", "target_field") 
    >>> print data
    data  = {
        original_ds : {
            key_a : {
                target_field: value
                ...
            }
        },
        destination_ds : {
            key_a : {
                target_field: value
                ...
            }
        } 
    }

    """
    for ident in data[destination_ds].keys():
        ip_address = data[original_ds][ident][field]
        data[destination_ds][ident][field] = ip_address
