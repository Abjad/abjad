from abjad import *


def test_Meter_numerator_01( ):
   '''
   Meters implement a read / write numerator.
   '''

   t = Meter(3, 8)

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Rational(3, 8)

   t.numerator = 4

   assert t.numerator == 4
   assert t.denominator == 8
   assert t.duration == Rational(1, 2)
