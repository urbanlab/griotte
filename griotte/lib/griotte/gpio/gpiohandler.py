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
from griotte.ws import WebSocket

try:
    import RPIO
except SystemError:
    logging.error("Unable to load RPIO. Are you using a Raspberry ?")
    pass

class GPIOHandler:
    """ GPIO handler

    Handles requests for the GPIO subsystem
    """

    # Pin to board
    PORTS = { 'io0'  : { 'pin' : 12 },
              'io1'  : { 'pin' : 11 },
              'io2'  : { 'pin' : 13 },
              'io3'  : { 'pin' : 15 },
              'dip0' : { 'pin' :  7 },
              'dip1' : { 'pin' : 16 } }


    def __init__(self):
        """ Initialize GPIO subsystem and install websocket handlers

        """
        self._ws = WebSocket(watchdog_interval=2)

        RPIO.setmode(RPIO.BOARD)

        # Install websocket & RPIO callbacks
        for port in self.PORTS:
            pin = self.PORTS[port]['pin']
            self._ws.add_listener("digital.command." + port + ".sample",
                                 self._sample)
            # self._ws.add_listener("digital.command." + port + ".edge",
            #                      self._edge, "both")
            # self._ws.add_listener("digital.command." + port + ".rising",
            #                      self._edge, "rising")
            # self._ws.add_listener("digital.command." + port + ".falling",
            #                      self._edge, "falling")
            self._ws.add_listener("digital.command." + port + ".profile",
                                 self._profile)
            logging.debug("installing RPIO handlers for pin %s", pin)
            RPIO.add_interrupt_callback(pin, self._edge)
            # For now, we just set everything to input with pull up
            # we'll fix that with profiles later
            RPIO.setup(pin, RPIO.IN,
                       pull_up_down=RPIO.PUD_UP,
                       debounce_timeout_ms=50)

        self.start()

    def _pin_to_port(self, pin):
        for p in PORTS:
            if PORTS[p]['pin'] == pin:
                return p

        return None

    def _sample(self, port, message):
        """ Request a single sample

        :param channel: The websocket channel containing the port to sample (io0-3)
        :type channel: str
        :param message: The message received over the wire
        :type message: dict -- should be empty

        """

        port = port.split('.')[2]
        logging.debug("sample request in port %s" % port)

        self._ws.send("digital.event." + port + ".sample",
                      { 'value' : RPIO.input(self.PORTS[port]['pin']) } )

    def _edge(self, gpio_id, value):
        """ Callback for RPIO on edge

        :param gpio_id: which GPIO triggered the edge condition
        :type gpio_id: int
        :param value: the current value for the pin
        :type value: int
        """
        port = self._pin_to_port(gpio_id)
        edge = None

        if not port:
            return

        if value == 0:
            edge = "falling"
        else:
            edge = "rising"

        self._ws.send("digital.event." + port + "." + edge, { 'value' : value} )


    def _profile(self, port, message):
        """ Sets profile for port

        :param port: The websocket channel containing the port to set the profile for (io0-3, dip0-1)
        :type port: str
        :param message: The message received over the wire
        :type message: dict -- shoud contain a profile, see :doc:profiles
        """
        port = port.split('.')[2]

        jp = message['profile']
        logging.debug("profile request for port %s with profile %s" % (port, jp['name']))

        # Unpack dict to keywork arguments
        profile = Profile(**jp)
        self.PORTS[port]['profile'] = profile

    def start(self):
        logging.info("Starting GPIOHandler's websocket thread")
        self._ws.start()
        logging.info("Starting GPIOHandler's RPIO interrupts thread")
        RPIO.wait_for_interrupts(threaded=True)

