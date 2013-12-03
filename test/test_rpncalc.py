# Tests for websockets

import unittest
import socket
import random
from math import hypot

from raspeomix.rpncalc import RPNCalc

a,b = 0,0
rpn = RPNCalc()

def get_rand(max=100):
    return random.random()*max

class RPNCalcTests(unittest.TestCase):

    def setUp(self):
        self.a,self.b = get_rand(), get_rand()
        self.rpn = RPNCalc()

    def try1(self, op, result):
        self.assertEqual(self.rpn.process(str(self.a) + " " + op), result)

    def try2(self, op, result):
        self.assertEqual(self.rpn.process(str(self.a) + " " + str(self.b) + " " + op), result)

    def test_init(self):
        self.assertTrue(isinstance(rpn, RPNCalc))

    def test_add(self):
        self.try2('+', self.a + self.b)

    def test_sub(self):
        self.try2('-', self.a - self.b)

    def test_mul(self):
        self.try2('*', self.a * self.b)

    def test_div(self):
        self.try2('/', self.a / self.b)

    def test_mod(self):
        self.try2('%', self.a % self.b)

    def test_pow(self):
        self.try2('**', self.a ** self.b)

    def test_hypot(self):
        self.try2('hyp', hypot(self.a,self.b))

    def test_and(self):
        self.a = int(self.a)
        self.b = int(self.b)
        self.try2('&', self.a & self.b)

    def test_or(self):
        self.a = int(self.a)
        self.b = int(self.b)
        self.try2('|', self.a | self.b)

    def test_xor(self):
        self.a = int(self.a)
        self.b = int(self.b)
        self.try2('^', self.a ^ self.b)

    def test_rshift(self):
        self.a = int(self.a)
        self.b = int(self.b)
        self.try2('>>', self.a >>  self.b)

    def test_lshift(self):
        self.a = int(self.a)
        self.b = int(self.b)
        self.try2('<<', self.a <<  self.b)

    def test_lt(self):
        self.try2('<', self.a < self.b)
        self.assertTrue(self.rpn.process("0 1 <"))
        self.assertFalse(self.rpn.process("1 0 <"))
        self.assertFalse(self.rpn.process("0 0 <"))

    def test_gt(self):
        self.try2('>', self.a > self.b)
        self.assertFalse(self.rpn.process("0 1 >"))
        self.assertTrue(self.rpn.process("1 0 >"))
        self.assertFalse(self.rpn.process("0 0 >"))

    def test_le(self):
        self.try2('<=', self.a <= self.b)
        self.assertTrue(self.rpn.process("0 1 <="))
        self.assertFalse(self.rpn.process("1 0 <="))
        self.assertTrue(self.rpn.process("0 0 <="))

    def test_ge(self):
        self.try2('>=', self.a >= self.b)
        self.assertFalse(self.rpn.process("0 1 >="))
        self.assertTrue(self.rpn.process("1 0 >="))
        self.assertTrue(self.rpn.process("0 0 >="))

    def test_eq(self):
        self.assertTrue(self.rpn.process("1 1 =="))
        self.assertTrue(self.rpn.process("0 0 =="))
        self.assertFalse(self.rpn.process("0 1 =="))
        self.assertFalse(self.rpn.process("1 0 =="))

    def test_ne(self):
        self.try2('!=', self.a != self.b)

    def test_invert(self):
        self.a = int(self.a)
        self.try1('~', ~self.a)


if __name__ == "__main__":
    unittest.main()

