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
import mcp342x as MCP342
import json
import pprint
pp = pprint.PrettyPrinter(depth=2)

"""
Messages:

/request/an/2 { "profile???" }
/message/an/0 { "value" : 146, "profile" : { "name" : "Maxborktik EZ-1", ... }}

All exchanged messages have a timestamp

"""
class Profile:
    def __init__(self, name, description='', units='', formula='x', valrange=[0, 1024], resolution='12bits'):
        self.name = name
        self.description = description
        self.units = units
        self.formula = formula
        self.range = valrange
        self.resolution = resolution

class AnalogDevice:
    """ ADC Interface """

    def __init__(self, device, profile):
        self.device = device
        self.profile  = profile

    def __repr__(self):
        return "AnalogDevice(%s,%s,%s,%s)" % (self.value('an0'),self.value('an1'),
                                              self.value('an2'),self.value('an3'))

    def value(self, channel):
        val = self.device.read_channel(channel, self.profile.resolution, gain='1x')
        # TODO: convert with formula & bound
        return val

if __name__ == "__main__":
    a = AnalogDevice(MCP342.MCP342x(), Profile('Identity'))
    while True:
        print("%s" % a)

