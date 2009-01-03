from abjad import *
import py.test


def test_meter_duration_01( ):
   '''
   Meters implement a read-only duration.
   '''

   t = Meter(3, 8)

   assert t.numerator == 3
   assert t.denominator == 8
   assert t.duration == Rational(3, 8)
   
   assert py.test.raises(AttributeError, 't.duration = (5, 16)')
