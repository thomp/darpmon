#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2016 David A. Thompson <thompdump@gmail.com>
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
import logging.handlers
lg = logging
# immediately configure the logger format
log_format = '%(message)s'
log_level = logging.INFO
lg.basicConfig(format=log_format,
               level=log_level,
               stream=sys.stdout)
dm_lg = lg

import json1
import util

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nConsider using 'sudo'.")

# check for executables busca relies on
if not util.which('arp-scan'):
    msg = json1.json_msg_executable_not_accessible('arp-scan')
    lg.error(msg)
    sys.exit(msg)

# establish configuration
config = None
config_file_location = os.path.expanduser("~/.darpmon.json")
if (os.path.exists(config_file_location)): 
    f=open(config_file_location)
    config_file_string = f.read()
    f.close()
    config = json.loads(config_file_string)
else:
    print "Config file %s not found",config_file_location

# establish configuration defaults
default_log_file_location = os.path.expanduser("~/.darpmon.log")
if not ('log_file' in config):
    config['log_file'] = default_log_file_location
default_scan_delay = 60
if not ('scan_delay' in config):
    config['scan_delay'] = default_scan_delay
    
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

def parse_and_log_raw_arp_scan_line(line,logger):
    ipv4_re = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ipv4 = ipv4_re.match(line)
    mac_re = re.compile("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})")
    mac = mac_re.search(line)
    date_string = str(time.time())
    json_encoded = json.dumps( {
        'd': date_string,
        'mac': mac.group(),
        'ipv4': ipv4.group()} )
    logger.info(json_encoded)

def parse_raw_arp_scan_string(raw_string,logger):
    discard_p = True
    lines = raw_string.splitlines()
    # discard lines through 'Starting...'
    # consume lines until blank line
    for line in lines:
        if (line[0:8] == "Starting"):
            discard_p = False
        elif ( not discard_p ):
            if (line and line[0].isdigit()):
                parse_and_log_raw_arp_scan_line(line,logger)
            else:
                discard_p = True

def main():
    """Handle command-line invocation."""
    global config
    global dm_lg
    parser = argparse.ArgumentParser(description="This is darpmon")
    parser.add_argument("-f", help="absolute path to log file", action="store", dest="log_file", type=str)
    parser.add_argument("-l", help="integer between 0 (verbose) and 51 (terse) defining logging", action="store", dest="log_level", type=int)
    args = parser.parse_args()
    if args.log_file:
        config['log_file'] = args.log_file
    if ('log_file' in config) and config['log_file']:
        dm_lg_handler = logging.handlers.RotatingFileHandler(
            filename=config['log_file'],
            maxBytes=400000,
            mode='a',
            backupCount=3)
        dm_lg = logging.getLogger("darpmon")
        dm_lg.addHandler(dm_lg_handler)
        dm_lg.setLevel(log_level)
        dm_lg_handler.setFormatter(logging.Formatter(log_format))
    while True:
        raw_scan_string = arp_scan()
        parse_raw_arp_scan_string(raw_scan_string,dm_lg)
        time.sleep(config['scan_delay'])

if __name__ == "__main__":
    main()
