# vim: ts=4:sw=4

from raspeomix.adc.profile import Profile
from raspeomix.adc.mcp342x import MCP342x

import pprint
pp = pprint.PrettyPrinter(indent=4)

class AnalogDevice:
    """ ADC Interface """
    channel = {}

    def __init__(self, device=MCP342x()):
        self.device = device
        self.profiles = dict()

        for chan in ['an0', 'an1', 'an2', 'an3']:
            self.profiles[chan] = Profile('Identity')

    def __repr__(self):
        for chan in ('an0', 'an1','an2','an3'):
            self.convert(chan)

        return "AnalogDevice(%s,%s,%s,%s)" % (self.convert('an0').value,
                                              self.convert('an1').value,
                                              self.convert('an2').value,
                                              self.convert('an3').value)

    def set_profile(self, channel, profile):
        if channel not in self.profiles.keys():
            raise ValueError('No such analog channel')

        self.profiles[channel] = profile

    def convert(self, chanidx):
        self.channel[chanidx] = self.device.read_channel(chanidx,
                                                         self.profiles[chanidx].resolution,
                                                         self.profiles[chanidx].gain)
        self.profiles[chanidx].value = self.channel[chanidx]
        return self.profiles[chanidx]
