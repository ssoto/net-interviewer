#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import logstash
import sys

host = 'localhost'

test_logger = logging.getLogger('python-logstash-logger')
test_logger.setLevel(logging.DEBUG)
test_logger.addHandler(logstash.LogstashHandler(host, 5959, version=1))
# test_logger.addHandler(logstash.TCPLogstashHandler(host, 5959, version=1))
test_logger.addHandler(logging.StreamHandler())

test_logger.error('python-logstash: test logstash error message.')
test_logger.info('python-logstash: test logstash info message.')
test_logger.warning('python-logstash: test logstash warning message.')

# add extra field to logstash message
extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}

test_logger.info('python-logstash: test extra fields', extra=extra)

class ClassName(object):
    """docstring for ClassName"""
    def __init__(self, logtash_server, logtash_port):
        super(ClassName, self).__init__()
        self.logtash_server = logtash_server
        self.logtash_port = logtash_port

        self.logger = logging.getLogger('python-logstash-logger')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logstash.LogstashHandler(host, logtash_port, logtash_server, version=1))


        