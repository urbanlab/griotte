# Tests for websockets

import unittest
import random
from raspeomix.adc import AnalogDevice
from raspeomix.adc import Profile

class FakeADC():
  def read_channel(self, *args):
    return random.random()*5 + 0.1

class AnalogDeviceTests(unittest.TestCase):
    def setUp(self):
        self.dev = AnalogDevice(FakeADC())

    def testIdentityRandom(self):
        self.assertTrue(self.dev.convert('an0').value > 0)
        self.assertTrue(self.dev.convert('an1').value > 0)
        self.assertTrue(self.dev.convert('an2').value > 0)
        self.assertTrue(self.dev.convert('an3').value > 0)

    def testProfile(self):
        doubler = Profile('Doubler', formula='$x 2 *')
        dev = AnalogDevice(FakeADC())
        dev.set_profile('an0', doubler)
        val = dev.convert('an0')
        self.assertTrue(2 * val.value == val.converted_value)

    def testWrongChannel(self):
        doubler = Profile('Doubler', formula='$x 2 *')
        dev = AnalogDevice(FakeADC())
        self.assertRaises(ValueError, dev.set_profile, 'an10', doubler)

if __name__ == "__main__":
    unittest.main()

