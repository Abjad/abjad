from abjad import *


def test_mathtools_scalar_divide_01( ):
   '''Divide can take integers.'''

   t = mathtools.scalar_divide(1, [1, 1, 2])

   assert len(t) == 3
   assert t[0] == 1 / 4.
   assert t[1] == 1 / 4.
   assert t[2] == 1 / 2.


def test_mathtools_scalar_divide_02( ):
   '''Divide can take rationals.'''

   t = mathtools.scalar_divide(Rational(1, 2), [1,1,2])

   assert len(t) == 3
   assert t[0] == Rational(1, 8)
   assert t[1] == Rational(1, 8)
   assert t[2] == Rational(1, 4)
