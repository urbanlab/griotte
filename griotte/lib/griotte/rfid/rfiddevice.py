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
import subprocess
import sys
import pexpect

"""
This is real crap
find a better way to read Tags
=> RFIDiot is not really usable
=> nfcpy has tons of deps

compile own binary from libnfc ?
"""

class RFIDDevice:
    _RFID_CMD = "/bin/bash -c \"/usr/local/bin/iso14443a-poller -d %s 2> /dev/null\""

    def __init__(self):
        """ Initializes RFID "device"
        """


    def start(self, observer_callback, delay=100):
        logging.debug("Starting RFIDDevice polling")

        logging.debug(self._RFID_CMD % delay)

        self._process = pexpect.spawn(self._RFID_CMD % delay, timeout=10 )

        while self._process:
            try:
                tag = self._process.readline().decode('ascii')
                if tag != '':
                    tag = tag.rstrip('\n').rstrip('\r')
                    logging.debug("Got tag %s" % tag)
                    observer_callback(tag)

            except pexpect.TIMEOUT:
                pass

        sleep(5)
        self.start(observer_callback, delay)



