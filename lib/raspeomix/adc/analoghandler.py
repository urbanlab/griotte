#
# (c) 2013-2014 ERASME
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
# along with Raspeomix. If not, see <http://www.gnu.org/licenses/>.

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

class AnalogHandler:
    def __init__(self):
        self.analogdevice = AnalogDevice()

        self.ws = WebSocket(watchdog_interval=2)

        for chan in self.analogdevice.device.channels():
            self.ws.add_listener('request.analog.' + chan,
                                 self.request, chan)

        self.sample_rate = None
        self.periodic_sampled_channels = []

        self.start()

    def request(self, channel, message):
        # Let's get the real analog channel from the path
        channel = channel[channel.rfind(':')+1:]
        logging.info("Request received for channel %s with message %s" % (channel, message))
        # Message types :
        # set_profile
        # get_value
        # periodic_sample
        if message['type'] == 'periodic_sample':
            logging.debug("periodic_sample request with sample_rate %s" % self.sample_rate)
            self.periodic_sampled_channels.append(channel)
            self.sample_rate = message['every']
        elif message['type'] == 'set_profile':
            jp = message['profile']
            logging.debug("set_profile request with profile %s" % jp['name'])
            # Unpack dict to keywork arguments
            profile = Profile(**jp)
            self.analogdevice.set_profile(channel, profile)

    def start(self):
        logging.info("Starting AnalogHandler's websocket")
        self.ws.start()

        logging.info("Starting sampling loop")
        while True:
            if self.sample_rate != None:
                sleep(self.sample_rate)
                # do sample
                for chan in self.periodic_sampled_channels:
                    logging.debug("Sampling %s" % chan)
                    self.ws.send("message.analog." + chan,
                                self.analogdevice.convert(chan).__dict__)




