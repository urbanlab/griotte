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

import quick2wire.i2c as i2c
import tornado.websocket
import json


"""
Messages:

/request/an/2 { "profile???" }
/message/an/0 { "value" : 146, "profile" : { "name" : "Maxborktik EZ-1", ... }}

All exchanged messages have a timestamp

"""

class MCP342x():
    """ ADC Interface """

    # Constants for configuration register, datasheet page 18
    #
    # Sample rate selection bits (S1-S0)
    RESOLUTION = {
        '12bits'  : 0b00000000,
        '14bits'  : 0b00000100,
        '16bits'  : 0b00001000,
        '18bits'  : 0b00001100,
        '240sps'  : 0b00000000,
        '60sps'   : 0b00000100,
        '15sps'   : 0b00001000,
        '3_75sps' : 0b00001100
    }

    # PGA settings
    GAIN = {
        '1x' : 0b00000000,
        '2x' : 0b00000001,
        '4x' : 0b00000010,
        '8x' : 0b00000011
    }

    # Channels
    CHANNEL = {
        'an0' : 0b00000000,
        'an1' : 0b00100000,
        'an2' : 0b01000000,
        'an3' : 0b01100000
    }

    # LSB in µV (cf datasheet table 4-1 p15)
    LSB = {
        '12bits'  : 1000,
        '14bits'  : 250,
        '16bits'  : 62.5,
        '18bits'  : 15.625,
        '240sps'  : 1000,
        '60sps'   : 250,
        '15sps'   : 62.5,
        '3_75sps' : 15.625
    }

    # Ready bit
    C_READY = 0b10000000
    # Single shot mode
    C_OC_MODE = 0b00010000

    # Resistors divider ratio (R20+R21)/R21 required to scale back input voltage -
    # see {https://raw.github.com/hugokernel/RaspiOMix/master/export/1.0.1/images/schema.png Schematic}
    #
    # @note Ratio for 4k7 / 10k : 3.3
    # @note Ratio for 6k8 / 10k : 2.471
    DIVIDER_RATIO = 3.3

    def __init__(self, address=0x6E, bus=i2c.I2CMaster() ):
        self.bus     = bus
        self.address = address

    def __repr__(self):
        return 'MCP342x(%s, {self})'.format(self=self)

    def read_channel(self, channel, resolution='12bits', gain='1x'):
        self._set_channel(channel, resolution, gain)

        # Check how many bytes we'll have to read
        # This depends on resolution
        bytes_to_read = 3
        if resolution == '18bits' or resolution == '3_75sps':
            # Read 4 bytes
            # The first byte should be all zeroes
            # The first bit of 4th byte (& 0x80) should be 0, indicating the
            # measure is ready (Cf datasheet page 19)
            bytes_to_read = 4

        bytes = [ 0x00 ] * bytes_to_read
        bytes = self.bus.transaction(i2c.reading(self.address, bytes_to_read))[0]
        # Repeat reading until ready bit is set
        while (bytes[bytes_to_read-1] & MCP342x.C_READY != 0):
            bytes = self.bus.transaction(i2c.reading(self.address, bytes_to_read))[0]

        if resolution in ('18bits', '3_75sps'):
            output_code = ((bytes[0] & 0b00000001) << 16) | (bytes[1] << 8) | bytes[2]
        elif resolution in ('16bits', '15sps'):
            output_code = ((bytes[0] & 0b01111111) << 8) | bytes[1]
        elif resolution in ('14bits', '60sps'):
            output_code = ((bytes[0] & 0b00011111) << 8) | bytes[1]
        elif resolution in ('12bits', '240sps'):
            output_code = ((bytes[0] & 0b00000111) << 8) | bytes[1]

        # Sign is always first bit of first byte, whatever the resolution
        # (Cf datasheet p22, table 5-3)
        if (bytes[0] & 0b10000000 != 0):
            output_code = ~(0x020000 - output_code)

        # We need the PGA factor, which is 2^PGA[gain]
        # and return voltage in volts
        # puts "DIVIDER_RATIO #{DIVIDER_RATIO} LSB[resolution] #{LSB[resolution]} output_code #{output_code} 2**PGA[gain] #{2**PGA[gain]}"
        return MCP342x.DIVIDER_RATIO * MCP342x.LSB[resolution] * (output_code / 2**MCP342x.GAIN[gain]) / 1000000


    def _set_channel(self, channel, resolution, gain):

        try:
            self.bus.transaction(i2c.writing_bytes(self.address,
                        MCP342x.C_READY | MCP342x.CHANNEL[channel] | MCP342x.C_OC_MODE | MCP342x.RESOLUTION[resolution] | MCP342x.GAIN[gain]))
        except KeyError:
            print("Error : this channel (%s) does not exist" % channel)
