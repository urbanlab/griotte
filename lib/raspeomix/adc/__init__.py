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

import tornado.websocket
from raspeomix.adc.mcp342x import MCP342x
from raspeomix.rpncalc import RPNCalc
import json
import pprint
from string import Template
pp = pprint.PrettyPrinter(depth=2)

"""
Messages:

/request/an/2 { "profile???" }
/message/an/0 { "value" : 146, "profile" : { "name" : "Maxborktik EZ-1", ... }}

All exchanged messages have a timestamp

"""
class Profile:
    def __init__(self, name, description='', units='', formula='$x', valrange=[0, 1024], resolution='12bits', gain='1x'):
        self.name = name
        self.description = description
        self.units = units
        self.formula = formula
        self.range = valrange
        self.resolution = resolution
        self.gain = gain
        self._raw_value = valrange[0]
        self.value = valrange[0]

    @property
    def value(self):
        return self._raw_value

    @value.setter
    def value(self, val):
        self._raw_value = val
        formula = Template(self.formula).substitute(x=val)
        self._converted_value = RPNCalc().process(formula)

    @property
    def converted_value(self):
        return self._converted_value

    @property
    def value_pair(self):
        return [ self._raw_value,
                 self._converted_value ]


class AnalogDevice:
    """ ADC Interface """
    channel = {}

    def __init__(self, device, profile):
        self.device = device
        self.profile  = profile

    def __repr__(self):
        return "AnalogDevice(%s,%s,%s,%s)" % (self.value('an0'),
                                              self.value('an1'),
                                              self.value('an2'),
                                              self.value('an3'))



    def convert(self, chanidx):
        self.channel[chanidx] = self.device.read_channel(chanidx,
                                                         self.profile.resolution,
                                                         self.profile.gain)
        self.profile.value = self.channel[chanidx]
        return self.profile

if __name__ == "__main__":
    from datetime import datetime

    a = AnalogDevice(MCP342x(), Profile('Identity'))
    print("%s" % a)




