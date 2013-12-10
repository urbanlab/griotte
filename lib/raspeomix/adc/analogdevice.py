# vim: ts=4:sw=4

from raspeomix.adc.profile import Profile
from raspeomix.adc.devices import *

class AnalogDevice:
    """ ADC Interface """

    def __init__(self, device=MCP342x()):
        self.device = device
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
