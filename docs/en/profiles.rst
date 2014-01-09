********
Profiles
********

Formulas
========

Profile formulas are expressed in RPN notation. The sensor raw value can be accessed with '$x'.
For instance, if you wan to write a profile that just doubles the value of the sensor and gets it's square root, the formula would be :

    $x 2 * sqrt

Stack operations
----------------

- "drop" : drops the last item on the stack
- "dup"  : duplicates the last item of the stack
- "swap" : swaps the last item and the previous item on the stack

Math constants
--------------

- ``pi`` : somewhere around 3.14
- ``e``  : base of natural logarithms

Math operations
---------------

Most of math operations are supported, including boolean ones. Check :mod:`griotte.rpncalc`.
for a complete and up to date list.
