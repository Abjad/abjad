from abjad import *
import py.test


def test_meter_duration_01( ):
   '''
   Meters implement a read-only duration.
   '''

   t = Meter(3, 8)

   assert t.duration == Rational(3, 8)
   assert py.test.raises(AttributeError, 't.duration = (5, 16)')


def test_meter_duration_02( ):
   '''
   Meters implement read-only duration.
   '''

   t = Meter(6, 16)

   assert t.duration == Rational(3, 8)
   assert py.test.raises(AttributeError, 't.duration = (5, 16)')
