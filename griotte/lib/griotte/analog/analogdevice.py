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

from griotte.analog.profile import Profile
from griotte.analog.devices import *

class AnalogDevice:
    def __init__(self, device=None):
        # using MCP342x() instead of None in the arguments breaks sphinx
        # thus, this construct
        self.device = device or MCP342x()
        self.profiles = dict()

        for chan in self.device.channels():
            self.profiles[chan] = Profile('Identity')

    def __repr__(self):
        str_repr = "AnalogDevice("

        for chan in self.device.channels():
            str_repr += ", " + self.convert(chan).value

        return str_repr + ")"

    def set_profile(self, channel, profile):
        if channel not in self.profiles.keys():
            raise ValueError('No such analog channel')

        self.profiles[channel] = profile

    def convert(self, chanidx):
        self.profiles[chanidx].value = self.device.read_channel(chanidx,
                                                         self.profiles[chanidx].resolution,
                                                         self.profiles[chanidx].gain)
        return self.profiles[chanidx]
