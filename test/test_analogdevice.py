# Tests for websockets

import unittest
import random

class FakeADC():
  def read_channel(self):
    return random.random()*5

class AnalogDeviceTests(unittest.TestCase):
    def testInit(self):
        self.failUnless(dev is AnalogDevice())

    def testIdentityRandom(self):
        dev = AnalogDevice(FakeADC(), Profile('Identity'))
        self.failUnless(dev.value('an0'))
        self.failUnless(dev.value('an1'))
        self.failUnless(dev.value('an2'))
        self.failUnless(dev.value('an3'))

if __name__ == "__main__":
    unittest.main()

