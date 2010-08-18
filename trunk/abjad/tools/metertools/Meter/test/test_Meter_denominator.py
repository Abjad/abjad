from abjad import *


def test_Meter_denominator_01( ):
   '''Meter are immutable.
   '''

   t = metertools.Meter(3, 8)

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Rational(3, 8)

#   t.denominator = 16
#
#   assert t.numerator == 3
#   assert t.denominator == 16
#   assert t.duration == Rational(3, 16)
