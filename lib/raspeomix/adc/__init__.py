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

from raspeomix.adc.devices import *
from raspeomix.adc.analogdevice import AnalogDevice
from raspeomix.adc.profile import Profile
from raspeomix.ws import WebSocket
from time import sleep

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

        self.ws = WebSocket(watchdog_interval=2)

        for chan in self.analogdevice.device.channels():
            self.ws.add_listener('request:analog:' + chan,
                                 self.request, chan)

        self.sample_rate = None
        self.periodic_sampled_channels = ()

        self.start()

    def request(self, channel, message):
        logging.info("Request received for channel %s with message %s" % (channel, message))


    def start(self):
        logging.info("Starting AnalogHandler's websocket")
        self.ws.start()

        logging.info("Starting sampling loop")
        while True:
            if self.sample_rate != None:
                sleep(self.sample_rate)
                # do sample
                for chan in self.periodic_sampled_channels:
                    value = self.analogdevice.convert(chan).value
                    ws.send("message:analog:" + chan,
                            { "value": value })


if __name__ == "__main__":
    import tornado.options
    tornado.options.parse_command_line()

    AnalogHandler()




