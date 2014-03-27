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

import serial, sys, time
import atexit

class DMXConnection(object):
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

    def __init__(self, comport=None):
        self._com = None
        self._dmx_frame = list()

      #setup channel output list
        for i in xrange (511):
            self._dmx_frame.append(0)

      #open com
        if comport is None:
            comport = "/dev/ttyUSB0"

        try:
            self._com = serial.Serial(comport, baudrate=self.COM_BAUD, timeout=self.COM_TIMEOUT)
        except:
            logging.error("Could not open COM%s, quitting handler" % comport)
            sys.exit(0)

        atexit.register(self.close)
        print "Opened %s" % (self._com.portstr)

    def set_channels(self, channels, val):
        for key in channels:
            chan = key
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
            for c in xrange (1, 512, 1):
                self._dmx_frame[c]=0
        else:
            for c in channels:
                self._dmx_frame[c]=0

        self._render()

    def _render(self):
    #  updates the dmx output from the USB DMX Pro with the values from self.dmx_frame
        packet = []
        packet.append(chr(self.START_VAL))
        packet.append(chr(self.LABELS['TX_DMX_PACKET']))
        packet.append(chr(len(self._dmx_frame) & 0xFF))
        packet.append(chr((len(self._dmx_frame) >> 8) & 0xFF))

        for j in xrange(len(self._dmx_frame)):
            packet.append(chr(self._dmx_frame[j]))

        packet.append(chr(self.END_VAL))

        self._com.write(''.join(packet))

    def close(self):
        self._com.close()

