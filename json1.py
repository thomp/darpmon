# -*- coding: utf-8 -*-

# (c) 2014,2015 David A. Thompson <thompdump@gmail.com>
#
# This file is part of Darpmon
#
# Darpmon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Darpmon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Darpmon. If not, see <http://www.gnu.org/licenses/>.
import json

#
# convenience functions for returning, as strings, JSON-encoded messages and data
#
def json_msg(code,message,outfile):
    """Return a string or, if outfile is a string, send to the file corresponding to outfile."""
    # if appendp is True (the default), create file if nonexistent; append if existent
    appendp=True
    if appendp:
        openMode='a+'
    else:
        openMode='w+'
    obj = {
        'code': code,
        'message': message
    }
    if outfile:
        with open(outfile, openMode) as outfp:
            json.dump(obj, outfp)
    else:
        return json.dumps(obj)

#
# messages
#
def json_msg_executable_not_accessible(executable_name):
    """EXECUTABLE_NAME is a string."""
    return json_msg(134,
             'The executable ' + executable_name + ' is not accessible. Is it installed?',
             False)

def json_msg_module_not_accessible(module_name):
    """MODULE_NAME is a string."""
    return json_msg(134,
             'The python module ' + module_name + ' is not accessible. Is it installed?',
             False)
