from raspeomix.rpncalc import RPNCalc
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
        self._raw_value = valrange[0]
        #self.value = valrange[0]

    def summary(self):
        return { "name": self.name,
                 "units": self.units,
                 "raw_value": self.value,
                 "value": self.converted_value }
    @property
    def value(self):
        return self._raw_value

    @value.setter
    def value(self, val):
        self._raw_value = val
        formula = Template(self.formula).substitute(x=val)
        self._converted_value = RPNCalc().process(formula)
        logging.debug("Setting value to %s, converted_value to %s" %
                      (self._raw_value, self._converted_value))

    @property
    def converted_value(self):
        return self._converted_value

    @property
    def value_pair(self):
        return [ self._raw_value,
                 self._converted_value ]


