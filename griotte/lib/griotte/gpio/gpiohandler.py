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
from griotte.handler import Handler

try:
    import RPIO
except SystemError:
    logging.error("Unable to load RPIO. Are you using a Raspberry ?")
    pass

class GpioHandler(Handler):
    """ GPIO handler

    Handles requests for the GPIO subsystem
    """

    # Pin to board
    # Note that RPIO prefers Board numbering
    # even if you use RPIO.setmode(RPIO.BOARD)
    # the callback will return BCM ports
    PORTS = { 'io0'  : { 'board' : 12, 'bcm' : 18 },
              'io1'  : { 'board' : 11, 'bcm' : 17 },
              'io2'  : { 'board' : 13, 'bcm' : 27 },
              'io3'  : { 'board' : 15, 'bcm' : 22 },
              'dip0' : { 'board' :  7, 'bcm' :  4 },
              'dip1' : { 'board' : 16, 'bcm' : 23 } }


    def __init__(self):
        """ Initialize GPIO subsystem and install websocket handlers

        """
        Handler.__init__(self)

        # Install websocket & RPIO callbacks
        for port in GpioHandler.PORTS:
            pin = GpioHandler.PORTS[port]['bcm']
            self.add_listener(port + ".sample")
            self.add_listener(port + ".profile")

            logging.debug("installing RPIO handlers for pin %s", pin)
            # For now, we just set everything to input with pull up
            # we'll fix that with profiles later
            RPIO.setup(pin, RPIO.IN,
                       pull_up_down=RPIO.PUD_UP)
            RPIO.add_interrupt_callback(pin, self._edge,
                                        debounce_timeout_ms=50)

        self.start()

    def _pin_to_port(self, pin):
        for p in GpioHandler.PORTS:
            if GpioHandler.PORTS[p]['bcm'] == pin:
                return p

        return None

    def _wscb_sample(self, port, message):
        """ Request a single sample

        :param channel: The websocket channel containing the port to sample (io0-3)
        :type channel: str
        :param message: The message received over the wire
        :type message: dict -- should be empty

        """
        port = port.split('.')[2]
        logging.debug("sample request in port %s" % port)

        boolval = RPIO.input(self.PORTS[port]['bcm'])

        self.send_event(port + ".sample",
                        { 'value' : boolval, 'raw_value': int(boolval) } )

    def _wscb_profile(self, port, message):
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

    def _edge(self, gpio_id, value):
        """ Callback for RPIO on edge

        :param gpio_id: which GPIO triggered the edge condition
        :type gpio_id: int
        :param value: the current value for the pin
        :type value: int
        """
        port = self._pin_to_port(gpio_id)
        edge = None
        logging.debug("edge detected on port %s" % port)

        if not port:
            return

        if value == 0:
            edge = "falling"
        else:
            edge = "rising"

        self.send(port + ".edge." + edge, { 'value': edge, 'raw_value': value })

    def start(self):
        logging.info("Starting GpioHandler's websocket thread")
        self._ws.start()
        logging.info("Starting GpioHandler's RPIO interrupts thread")
        RPIO.wait_for_interrupts(threaded=False)

