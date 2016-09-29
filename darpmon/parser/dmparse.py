#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, 2016 David A. Thompson <thompdump@gmail.com>

# parse darpmon log

import argparse
import json
import os
import string
import sys
import time

def hrm_def_make_identifier(config):
    use_nicks = True
    if ('use_nicks' in config):
        use_nicks = config['use_nicks']
    if (use_nicks and ('nicks' in config)):
        def make_identifier(mac):
            if (mac in config['nicks']):
                return config['nicks'][mac]
            else:
                return mac
    else:
        def make_identifier(mac):
            return mac
    return make_identifier

def human_readable_macs(macs,config):
    make_identifier = hrm_def_make_identifier(config)
    t = string.Template('${identifier} on for ${minDelta} min (${on_at} to ${off_at}) [${IP}]\n')
    for mac in macs:
        record = macs[mac]
        first_time_raw = record['firstTime']
        last_time_raw = record['lastTime']
        first_time = int(float(first_time_raw))
        last_time = int(float(last_time_raw))
        sec_delta = last_time - first_time
        min_delta = sec_delta / 60
        # use gmtime if time_format is 'UTC'
        # use localtime if time_format is 'localtime'
        readable_first_time = time.asctime(time.localtime(first_time))
        readable_last_time = time.asctime(time.localtime(last_time))
        identifier = make_identifier(mac)
        ipv4 = record['ipv4'] 
        sys.stdout.write(t.substitute(identifier=identifier,
                                      minDelta=min_delta,
                                      on_at=readable_first_time,
                                      off_at=readable_last_time,
                                      IP=ipv4
        ))

def parse_line(line,macs):
    """LINE is a string representing a single, raw line from the darpmon log."""
    obj = json.loads(line)
    mac = obj['mac']
    if (mac in macs):
        macs[mac]['lastTime']=obj['d']
    else:
        macs[mac]={
            'ipv4': obj['ipv4'],
            'firstTime': obj['d'],
            'lastTime': obj['d']
        }             
                                    
def main():
    """Handle command-line invocation."""
    parser = argparse.ArgumentParser(description="This is dmparse")
    parser.add_argument("input_files", help="one or more input (PDF) files", nargs="+", type=str)
    args = parser.parse_args()
    input_files = args.input_files
    #
    # deal with config file ~/.dmparserc.json
    #
    config = None
    config_file_location = os.path.expanduser("~/.dmparserc.json")
    if (os.path.exists(config_file_location)): 
        f=open(config_file_location)
        config_file_string = f.read()
        f.close()
        config = json.loads(config_file_string)        
    # keys are mac addresses
    # value has structure
    # { firstTime:             ,
    #   lastTime:              ,
    #   ipv4:                   }
    macs = {}
    # for each mac address
    # - look for when specific mac address first shows up
    # - look for when specific mac address appears to leave
    f=open(input_files[0],'r')
    for line in f.readlines():
        parse_line(line,macs)
    f.close()
    # output in manner user would like (overall format = JSON, human readable, ...)
    # - as JSON:
    #sys.stdout.write(str(macs))
    # - as human-readable summary
    human_readable_macs(macs,config)
    
if __name__ == "__main__":
    main()
