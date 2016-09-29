#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2016 David A. Thompson <thompdump@gmail.com>

# respond to HTTP GET request at device

# run from top-level dir with
#     sudo python -m darpmon.server.server

import BaseHTTPServer
import StringIO
import time

import darpmon.darpmon

import darpmon.parser.parser
#print dir(darpmon.parser.parser)

# 'localhost'
HOST_NAME = ''
PORT_NUMBER = 80

class DmHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers() 
        macs = darpmon.parser.parser.build_macs(darpmon.darpmon.config['log_file'])
        output = StringIO.StringIO()
        darpmon.parser.parser.human_readable_macs(macs,output.write)
        s.wfile.write(output.getvalue())
        # Close object and discard memory buffer --
        # .getvalue() will now raise an exception.
        output.close()

def start_server ():
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), DmHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print "exception"
        print e
    httpd.server_close()

if __name__ == "__main__":
    start_server()
