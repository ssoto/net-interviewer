#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import logging
logging.basicConfig( format='%(asctime)s - %(pathname)s:%(lineno)d : %(levelname)s  : %(message)s', 
                     level=logging.DEBUG)


def get_config(config_file_path):
    
    config = ConfigParser.ConfigParser()
    config.read(config_file_path)
    options_dict = {}
    
    for section in config.sections():
        section_options = {}
        for option in config.options(section):
            section_options[option] = config.get(section, option)
        options_dict[section] = section_options
    return options_dict

def exist_section(config_file_path, section):
    config = ConfigParser.ConfigParser()
    config.read(config_file_path)
    return config.has_section(section)


if __name__ == "__main__":
    import pprint
    config_file = './net_interviewer.conf'
    section = 'Others'
    logging.debug( "Exist section '%s' => %s" %(section, exist_section(config_file, section)))
    all_stuff = get_config( config_file)
    pprint.pprint(all_stuff)
