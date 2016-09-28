#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, 2016 David A. Thompson <thompdump@gmail.com>

# parse darpmon log

import argparse
import json
import string
import time
import sys

def human_readable_macs(macs):
    t = string.Template('${MAC} on for ${minDelta} min (${on_at} to ${off_at})\n')
    for mac in macs:
        record = macs[mac]
        first_time_raw = record['firstTime']
        last_time_raw = record['lastTime']
        first_time = int(float(first_time_raw))
        last_time = int(float(last_time_raw))
        sec_delta = last_time - first_time
        min_delta = sec_delta / 60
        readable_first_time = time.asctime(time.gmtime(first_time))
        readable_last_time = time.asctime(time.gmtime(last_time))
        sys.stdout.write(t.substitute(MAC=mac,
                                      minDelta=min_delta,
                                      on_at=readable_first_time,
                                      off_at=readable_last_time ))

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
    human_readable_macs(macs)
    
if __name__ == "__main__":
    main()
