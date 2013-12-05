# Tests for websockets

import unittest
import socket
from random import *
from math import *

from raspeomix.rpncalc import RPNCalc

a,b = 0,0
rpn = RPNCalc()

def get_rand(max=100):
    return random.random()*max

class RPNCalcTests(unittest.TestCase):

    def setUp(self):
        self.a,self.b = random()*100, random()*100
        self.rpn = RPNCalc()

    def try0(self, op, result):
        self.assertEqual(self.rpn.process(op), result)

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

    def test_sin(self):
        self.a = random() % 360
        self.try1('sin', sin(self.a))

    def test_cos(self):
        self.a = random() % 360
        self.try1('cos', cos(self.a))

    def test_tan(self):
        self.a = random() % 360
        self.try1('tan', tan(self.a))

    def test_asin(self):
        self.a = random()
        self.try1('asin', asin(self.a))

    def test_acos(self):
        self.a = random()
        self.try1('acos', acos(self.a))

    def test_atan(self):
        self.a = random()
        self.try1('atan', atan(self.a))

    def test_sinh(self):
        self.try1('sinh', sinh(self.a))

    def test_cosh(self):
        self.try1('cosh', cosh(self.a))

    def test_tanh(self):
        self.try1('tanh', tanh(self.a))

    def test_asinh(self):
        self.a = random()
        self.try1('asinh', asinh(self.a))

    def test_acosh(self):
        self.a = 1+random()*5
        self.try1('acosh', acosh(self.a))

    def test_atanh(self):
        self.a = random()
        self.try1('atanh', atanh(self.a))

    def test_sqrt(self):
        self.try1('sqrt', sqrt(self.a))

    def test_log(self):
        self.try1('log', log(self.a))

    def test_exp(self):
        self.try1('exp', exp(self.a))

    def test_floor(self):
        self.try1('floor', floor(self.a))

    def test_ceil(self):
        self.try1('ceil', ceil(self.a))

    def test_erf(self):
        self.try1('erf', erf(self.a))

    def test_erfc(self):
        self.try1('erfc', erfc(self.a))

    def test_fact(self):
        self.a = int(self.a)
        self.try1('!', factorial(self.a))

    def test_fabs(self):
        self.try1('abs', fabs(self.a))

    def test_degrees(self):
        self.a %= 360
        self.try1('deg', degrees(self.a))

    def test_radians(self):
        self.a %= 2*pi
        self.try1('rad', radians(self.a))

    def test_pi(self):
        self.try0('pi', pi)

    def test_e(self):
        self.try0('e', e)

    def test_swap(self):
        # Stack :
        # a
        # b a
        # SWAP b a
        # a b
        self.try2('s', self.a)

    def test_drop(self):
        # Stack :
        # a
        # b a
        # DROP b a
        # a
        self.try2('d', self.a)

    def test_integer_zero(self):
        self.a = 0
        self.try0("%s" % self.a, self.a)

    def test_decimal_zero(self):
        self.a = 0.0
        self.try0("%s" % self.a, self.a)

if __name__ == "__main__":
    unittest.main()

