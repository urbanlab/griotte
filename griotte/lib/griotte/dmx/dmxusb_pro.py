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

# Code initially from https://github.com/c0z3n/pySimpleDMX

import serial, sys, time
import logging
import atexit

class DMXUniverse(object):
    START_VAL = 0x7E
    END_VAL = 0xE7

    COM_BAUD = 57600
    COM_TIMEOUT = 1
    COM_PORT = 7

    LABELS = {
                'GET_WIDGET_PARAMETERS' :3,  #unused
                'SET_WIDGET_PARAMETERS' :4,  #unused
                'RX_DMX_PACKET'         :5,  #unused
                'TX_DMX_PACKET'         :6,
                'TX_RDM_PACKET_REQUEST' :7,  #unused
                'RX_DMX_ON_CHANGE'      :8,  #unused
              }

    def __init__(self, com_start=0):
        self._com = None
        self._dmx_frame = list()

        for num in range(com_start, 4):
            comport = "/dev/ttyUSB%s" % num

            try:
                self._com = serial.Serial(comport, baudrate=self.COM_BAUD, timeout=self.COM_TIMEOUT)
                break
            except:
                logging.warning("Could not open port %s" % comport)

        logging.info("Serial port %s opened (%s) " % (comport, self._com.portstr))

        # "Ensure" port is properly closed on exit
        atexit.register(self.close)

        # Setup channel list
        for i in range (511):
            self._dmx_frame.append(0)

    def set_channels(self, channels):
        for key in channels:
            chan = int(key)
            val = channels[key]

            if (chan > 512) or (chan < 1):
                logging.error("Invalid channel %s", chan)
            else:
                if val > 255: val=255
                if val < 0: val=0

            self._dmx_frame[chan] = val

        self._render()

    def clear_channels(self, channels=[]):
    #  clears all channels to zero. blackout.
    #  with optional channel argument, clears only one channel
        if len(channels) == 0:
            logging.debug("No channels received, full blackout")
            for c in range (0, 511):
                self._dmx_frame[c] = 0
        else:
            logging.debug("Channels received, selective blackout")
            for c in channels:
                self._dmx_frame[int(c)] = 0

        self._render()

    def _render(self):
    #  updates the dmx output from the USB DMX Pro with the values from self.dmx_frame
        packet = bytearray()
        packet.append(self.START_VAL)
        packet.append(self.LABELS['TX_DMX_PACKET'])
        packet.append(len(self._dmx_frame) & 0xFF)
        packet.append((len(self._dmx_frame) >> 8) & 0xFF)

        for j in range(len(self._dmx_frame)):
            packet.append(self._dmx_frame[j])

        packet.append(self.END_VAL)

        self._com.write(packet)

    def close(self):
        self._com.close()

