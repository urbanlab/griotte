#
# (c) 2013 ERASME
#
# This file is part of Raspeomix
#
# Raspeomix is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Raspeomix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from raspeomix.adc.mcp342x import MCP342x
from raspeomix.adc.analogdevice import AnalogDevice
from raspeomix.adc.profile import Profile
from raspeomix.ws import WebSocket
import logging
import json

"""
Messages:

request:analog:2 { "profile???" }
message:analog:0 { "value" : 146, "profile" : { "name" : "Maxborktik EZ-1", ... }}

All exchanged messages have a timestamp

"""
CHANNEL='an'

class AnalogHandler:
    def __init__(self):
        self.analogdevice = AnalogDevice()

        self.ws = WebSocket(watchdog_interval=10)
        self.ws.add_listener('request:analog:0', self.request, 0)
        self.ws.add_listener('request:analog:1', self.request, 1)
        self.ws.add_listener('request:analog:2', self.request, 2)
        self.ws.add_listener('request:analog:3', self.request, 3)

    def request(self, channel, message):
        logging.info("Request received for channel %s with message %s" % (channel, message))



if __name__ == "__main__":
    AnalogHandler()




