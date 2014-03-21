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

"""
"""

class RFIDDevice:
    _TAG_REXP = re.compile(b".*UID\s.*: (\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)")

    def __init__(self):
        """ Initializes RFID "device"
        """
        self._process = subprocess.Popen('ncf-poll', shell=False,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.DEVNULL)

    def start(self, observer_callback):
        logging.info("Starting RFIDDevice polling")

        while self._process.:
            matches = self._TAG_REXP.match(self._process.stdout.readline())
            if matches:
                logging.debug("Got tag")
                observer_callback("".join(matches.groups()))




