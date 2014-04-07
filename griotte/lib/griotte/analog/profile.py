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

from griotte.rpncalc import RPNCalc
from string import Template

import logging

class Profile:
    def __init__(self, name='Identity', description='', units='', formula='$x', valrange=[0, 1024], resolution='12bits', gain='1x'):
        self.name = name
        self.description = description
        self.units = units
        self.formula = formula
        self.range = valrange
        self.resolution = resolution
        self.gain = gain
        self.raw_value = self.converted_value = valrange[0]
        #self.value = valrange[0]

    @property
    def value(self):
        return self.raw_value

    @value.setter
    def value(self, val):
        self.raw_value = val
        formula = Template(self.formula).substitute(x=val)
        self.converted_value = RPNCalc().process(formula)
        logging.debug("Setting value to %s, converted_value to %s" %
                      (self.raw_value, self.converted_value))

    @property
    def value_pair(self):
        return [ self.raw_value,
                 self.converted_value ]


