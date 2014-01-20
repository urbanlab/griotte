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

from griotte.adc.analogdevice import AnalogDevice
from griotte.adc.profile import Profile
from griotte.ws import WebSocket
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
        """ Initialize ADc subsystem and install websocket handlers

        AnalogHandler only listens to periodic_sample and profile for now.
        """
        self.analogdevice = AnalogDevice()

        self.ws = WebSocket(watchdog_interval=2)

        for chan in self.analogdevice.device.channels():
            self.ws.add_listener("analog.command." + chan + ".periodic_sample",
                                 self._periodic_sample)
            self.ws.add_listener("analog.command." + chan + ".profile",
                                 self._profile)

        self.sample_delay = 1
        self.periodic_sampled_channels = []

        self.start()

    def _periodic_sample(self, channel, message):
        """ Start periodic sampling for channel

        :param channel: The channel to sample (an0-3)
        :type channel: str
        :param message: The message received over the wire
        :type message: dict -- shoud contain `every` key

        ..note :: When this method is called several times, the lowest value
                  for sampling period will be used
        """

        channel = channel.split('.')[2]

        # If faster samples are requested, we update our sampling rate
        # Sampling rate is the same for all channels !
        if self.sample_delay > message['every']:
            self.sample_delay = message['every']

        logging.debug("periodic_sample request in channel %s with sample_delay %s" % (channel, self.sample_delay))

        if channel not in self.periodic_sampled_channels:
            self.periodic_sampled_channels.append(channel)

    def _profile(self, channel, message):
        """ Sets profile for channel

        :param channel: The channel for which the profile will be set (an0-3)
        :type channel: str
        :param message: The message received over the wire
        :type message: dict -- shoud contain a profile, see :doc:profiles
        """
        jp = message['profile']
        logging.debug("profile request with profile %s" % jp['name'])
        # Unpack dict to keywork arguments
        profile = Profile(**jp)
        self.analogdevice.set_profile(channel, profile)

    def start(self):
        logging.info("Starting AnalogHandler's websocket")
        self.ws.start()

        logging.info("Starting sampling loop")
        while True:
            if self.sample_delay != None:
                sleep(float(self.sample_delay))
                # do sample
                for chan in self.periodic_sampled_channels:
                    logging.debug("Sampling %s" % chan)
                    self.ws.send("analog.event." + chan + ".sample",
                                self.analogdevice.convert(chan).__dict__)




