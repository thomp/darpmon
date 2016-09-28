#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, 2016 David A. Thompson <thompdump@gmail.com>
#
# This file is part of darpmon
#
# darpmon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# darpmon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with darpmon. If not, see <http://www.gnu.org/licenses/>.

#
# use: sudo python darpmon.py -l 0
#

import argparse
import json
import os
import re
import subprocess
import sys
import time

import logging
import logging.config
lg = logging
# and immediately configure the logger format
log_format = '%(message)s'
#json_log_format = '{d:%(asctime)s m:%(message)s}'
lg.basicConfig(format=log_format,level=logging.INFO,stream=sys.stdout)

import json1
import util

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nConsider using 'sudo'.")

# check for executables busca relies on
if not util.which('arp-scan'):
    msg = json1.json_msg_executable_not_accessible('arp-scan')
    lg.error(msg)
    sys.exit(msg)

def arp_scan():
    try:
        return_string = subprocess.check_output(
            # --quiet
            # responses have format <IP Address> <Hardware Address> <Vendor Details>
            ["arp-scan", "--localnet"],
            shell=False)
        return return_string
    except CalledProcessError as e: 
        msg = "error"
        #msg = json1.json_msg_module_not_accessible('PyPDF2') #json1.json_failed_to_convert_pdf(None,pdf_file)
        lg.error(msg)
        sys.exit(e.returncode)

def parse_and_log_raw_arp_scan_line(line):
    ipv4_re = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ipv4 = ipv4_re.match(line)
    mac_re = re.compile("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})")
    mac = mac_re.search(line)
    date_string = str(time.time())
    json_encoded = json.dumps( {
        'd': date_string,
        'mac': mac.group(),
        'ipv4': ipv4.group()} )
    lg.info(json_encoded)

def parse_raw_arp_scan_string(raw_string):
    discard_p = True
    lines = raw_string.splitlines()
    # discard lines through 'Starting...'
    # consume lines until blank line
    for line in lines:
        if (line[0:8] == "Starting"):
            discard_p = False
        elif ( not discard_p ):
            if (line and line[0].isdigit()):
                parse_and_log_raw_arp_scan_line(line)
            else:
                discard_p = True

def main():
    """Handle command-line invocation."""
    parser = argparse.ArgumentParser(description="This is darpmon")
    #parser.add_argument("-f", help="absolute path to log file", action="store", dest="log_file", type=str)
    parser.add_argument("-l", help="integer between 0 (verbose) and 51 (terse) defining logging", action="store", dest="log_level", type=int)
    args = parser.parse_args()
    #
    # define logging (level, file, message format, ...)
    #
    log_level = args.log_level
    if isinstance(log_level, int) and log_level >= 0 and log_level <= 51:
        log_level = log_level
    else:
        # standard python default
        #log_level = logging.WARN
        # since this function doesn't necessarily exit quickly
        log_level = logging.INFO
    #if args.log_file:
    #    logfile = args.log_file
    #else:
    #    logfile = 'darpmon.log'
    debug_log_format = '%(levelname)s:%(funcName)s:%(message)s'
    json_log_format = '%(message)s'
    #lg.basicConfig(filename=logfile, filemode='w', level=log_level, format=json_log_format)
    # number of seconds between ARP scans
    period=60
    while True:
        raw_scan_string = arp_scan()
        parse_raw_arp_scan_string(raw_scan_string)
        time.sleep(20)
    
if __name__ == "__main__":
    main()
