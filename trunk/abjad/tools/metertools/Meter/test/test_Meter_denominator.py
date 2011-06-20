from abjad import *
from abjad.tools import metertools


def test_Meter_denominator_01( ):
   '''Meter are immutable.
   '''

   t = metertools.Meter(3, 8)

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Duration(3, 8)

#   t.denominator = 16
#
#   assert t.numerator == 3
#   assert t.denominator == 16
#   assert t.duration == Duration(3, 16)
