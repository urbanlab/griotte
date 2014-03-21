#
# (c) 2013-2014 ERASME
#
# This file is part of griotte
#
# griotte is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# griotte is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with griotte. If not, see <http://www.gnu.org/licenses/>.


import logging
import re
import subprocess
import sys

"""
This is real crap
find a better way to read Tags
=> RFIDiot is not really usable
=> nfcpy has tons of deps

compile own binary from libnfc ?
"""

class RFIDDevice:
    _TAG_REXP = re.compile(b".*UID\s.*: (\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)")

    def __init__(self):
        """ Initializes RFID "device"
        """


    def start(self, observer_callback):
        logging.debug("(Re)starting RFIDDevice polling")

        self._process = subprocess.Popen('nfc-poll', shell=False,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)

        while True:
            line = self._process.stdout.readline()
            matches = self._TAG_REXP.match(line)
            if matches:
                tag = ""
                for m in matches.groups():
                    tag += m.decode('ascii')

                logging.debug("Got tag %s" % tag)
                observer_callback(tag)

                self._process.wait()
                self.start(observer_callback)


