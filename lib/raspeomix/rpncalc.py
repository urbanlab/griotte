# Part of this code is Copyright (C) 2010, Paul Lutus
# http://www.arachnoid.com/python/RPNCalc_program.html

import sys, re, readline, types
from math import *
from operator import *

class RPNCalc:
    def found(self,s,tup):
        for item in tup:
            if(s == item[0]):
                self.node = item
                return True
        return False

    def __init__(self, debug=False):
        self.stack = []
        self.debug = debug

        self.com2args = (
            ("+"   , add,        "y + x"),
            ("-"   , sub,        "y - x"),
            ("*"   , mul,        "y * x"),
            ("/"   , truediv,    "y / x"),
            ("%"   , fmod,       "y % x"),
            ("**"  , pow,       "y ** x"),
            ("hyp" , hypot, "hypot(x,y)"),
            ("&"   , and_,       "x & y"),
            ("|"   , or_,        "y | x"),
            ("^"   , xor,        "y ^ x"),
            (">>"  , rshift,    "y >> x"),
            ("<<"  , lshift,    "y << x"),
            ("<"   , lt,         "y < x"),
            (">"   , gt,         "y > x"),
            ("<="  , le,        "y <= x"),
            (">="  , ge,        "y >= x"),
            ("=="  , eq,        "y == x"),
            ("!="  , ne,        "y != x"),
        )

        self.com1arg = (
            ("sin"  ,sin,        "sin(x)"),
            ("cos"  ,cos,        "cos(x)"),
            ("tan"  ,tan,        "tan(x)"),
            ("asin" ,asin,      "asin(x)"),
            ("acos" ,acos,      "acos(x)"),
            ("atan" ,atan,      "atan(x)"),
            ("sinh" ,sinh,      "sinh(x)"),
            ("cosh" ,cosh,      "cosh(x)"),
            ("tanh" ,tanh,      "tanh(x)"),
            ("asinh",asinh,    "asinh(x)"),
            ("acosh",acosh,    "acosh(x)"),
            ("atanh",atanh,    "atanh(x)"),
            ("sqrt" ,sqrt,      "sqrt(x)"),
            ("log"  ,log,        "log(x)"),
            ("exp"  ,exp,        "exp(x)"),
            ("ceil" ,ceil,      "ceil(x)"),
            ("floor",floor,    "floor(x)"),
            ("erf"  ,erf,        "erf(x)"),
            ("erfc" ,erfc,      "erfc(x)"),
            ("!"    ,factorial,      "x!"),
            ("abs"  ,fabs,          "|x|"),
            ("deg"  ,degrees,"degrees(x)"),
            ("rad"  ,radians,"radians(x)"),
            ("~"    ,invert,        "~ x"),
        )

        self.coms = (
            ("pi", lambda: self.stack.insert(0,pi),"Pi"),
            ("e" , lambda: self.stack.insert(0,e),"e (base of natural logarithms)"),
            ("d" , lambda: self.stack.pop(0),"Drop x"),
            ("s" , lambda: self.stack.insert(0,self.stack.pop(1)),"Swap x <-> y"),
        )

    def dump_stack(self):
        print("---stack bottom---")

        for e in reversed(self.stack):
            print (e)
        print("\n---stack top---")

    def process(self, expression):
        spregex = re.compile("\s+")

        if self.debug:
            print("expr:%s" % expression)

        for tok in spregex.split(expression):
            try:
                # parsing a number
                # let's try to stick to ints if possible
                if (int(float(tok)) != float(tok)):
                    self.stack.insert(0,float(tok))
                else:
                    self.stack.insert(0,int(tok))

                if self.debug:
                    self.dump_stack()
            except: # it's not a number
                try: # look for command
                    if (self.found(tok, self.com2args)):
                        self.stack.insert(0,self.node[1](self.stack.pop(1),self.stack.pop(0)))
                    elif (self.found(tok, self.com1arg)):
                        self.stack.insert(0,self.node[1](self.stack.pop(0)))
                    elif (self.found(tok, self.coms)):
                        self.node[1]()
                    else:
                        print("Error: token \"%s\" not found!" % tok)

                    if self.debug:
                        self.dump_stack()
                except:
                    print("Error:", sys.exc_info()[0])

        return self.stack[0]


if __name__ == "__main__":
    expr = sys.argv[1]
    a = RPNCalc().process(expr)
    print("%s => %s" % (expr, a))
