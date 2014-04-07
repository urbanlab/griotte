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

from griotte.rfid.rfiddevice import RfidDevice

from griotte.handler import Handler

import logging
import json

"""
"""

class RfidHandler(Handler):
    def __init__(self):
        """ Initializes RFID "device"
        """
        Handler.__init__(self)

        self._rfiddevice = RfidDevice()
        self.start()

    def start(self):
        logging.info("Starting RFIDDevice")
        self._ws.start(detach=False)
        self._rfiddevice.start(self.send_tag)

    def send_tag(self, tag):
        logging.info("Sending tag %s" % tag)
        self.send_event("rfid.event.tag",
                      { 'tag' : tag } )




