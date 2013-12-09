# vim: ts=4:sw=4

from raspeomix.adc.profile import Profile

class AnalogDevice:
    """ ADC Interface """
    channel = {}

    def __init__(self, device, profile):
        self.device = device
        self.profile  = profile

    def __repr__(self):
        for chan in ('an0', 'an1','an2','an3'):
          self.convert(chan)

        return "AnalogDevice(%s,%s,%s,%s)" % (self.convert('an0').value,
                                              self.convert('an1').value,
                                              self.convert('an2').value,
                                              self.convert('an3').value)

    def convert(self, chanidx):
        self.channel[chanidx] = self.device.read_channel(chanidx,
                                                         self.profile.resolution,
                                                         self.profile.gain)
        self.profile.value = self.channel[chanidx]
        return self.profile
