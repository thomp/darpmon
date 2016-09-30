#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2016 David A. Thompson <thompdump@gmail.com>

# parse darpmon log

import argparse
import json
import os
import string
import sys
import time

import darpmon.darpmon

# f_out is a function which accepts a single argument, a string
def human_readable_macs(macs,f_out):
    make_identifier = hrm_def_make_identifier()
    t = string.Template('${identifier} on for ${minDelta} min (${on_at} to ${off_at}) [${IP}]\n')
    for mac in macs:
        record = macs[mac]
        intervals = record['intervals']
        while intervals:
            last_time = intervals.pop()
            first_time = intervals.pop()
            sec_delta = last_time - first_time
            min_delta = sec_delta / 60
            # use gmtime if time_format is 'UTC'
            # use localtime if time_format is 'localtime'
            readable_first_time = time.asctime(time.localtime(first_time))
            readable_last_time = time.asctime(time.localtime(last_time))
            identifier = make_identifier(mac)
            ipv4 = record['ipv4']
            out_string = t.substitute(identifier=identifier,
                                      minDelta=min_delta,
                                      on_at=readable_first_time,
                                      off_at=readable_last_time,
                                      IP=ipv4)
            f_out(out_string)

def build_macs(input_file):
    """Analyze log file input_file."""
    macs = {}
    f=open(input_file,'r')
    for line in f.readlines():
        parse_line(line,macs)
    f.close()
    return macs
        
def hrm_def_make_identifier():
    use_nicks = True
    if ('use_nicks' in darpmon.darpmon.config):
        use_nicks = darpmon.darpmon.config['use_nicks']
    if (use_nicks and ('nicks' in darpmon.darpmon.config)):
        def make_identifier(mac):
            if (mac in darpmon.darpmon.config['nicks']):
                return darpmon.darpmon.config['nicks'][mac]
            else:
                return mac
    else:
        def make_identifier(mac):
            return mac
    return make_identifier

def parse_line(line,macs):
    """LINE is a string representing a single, raw line from the darpmon log."""
    # number of seconds at which a device is considered absent (has 'left' the LAN)
    absent_at = 240
    obj = json.loads(line)
    mac = obj['mac']
    if (mac in macs):
        # 'intervals' slot holds a list of the form
        # [ onTime0, offTime0, ... onTimeN, offTimeN ]
        # where times are UNIX times (epoch/POSIX) and where
        # the values are ascending (most recent are last in the list)
        lastTime = int(float(macs[mac]['intervals'][-1]))
        thisTime = int(float(obj['d']))
        if ( thisTime - lastTime > absent_at ):
            macs[mac]['intervals'].append(thisTime)
            macs[mac]['intervals'].append(thisTime)
        else:
            macs[mac]['intervals'][-1] = thisTime
    else:
        macs[mac]={
            'ipv4': obj['ipv4'],
            'intervals': [ int(float(obj['d'])), int(float(obj['d'])) ]
        }             
                                    
def main():
    """Handle command-line invocation."""
    parser = argparse.ArgumentParser(description="This is dmparse")
    parser.add_argument("input_file", help="an input file", nargs="?", type=str)
    args = parser.parse_args()
    # determine location of input file
    input_file = None
    if 'log_file' in darpmon.darpmon.config:
        input_file = darpmon.darpmon.config['log_file']
    if args.input_file:
        input_file = args.input_file
        config['log_file'] = input_file
    if not input_file:
        sys.exit("Must specify an input file")
    macs = build_macs(input_file)
    # output in manner user would like (overall format = JSON, human readable, ...)
    # - as JSON:
    #sys.stdout.write(str(macs))
    # - as human-readable summary
    human_readable_macs(macs,sys.stdout.write)
              
if __name__ == "__main__":
    main()
