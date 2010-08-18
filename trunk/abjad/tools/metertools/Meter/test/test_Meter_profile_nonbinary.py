from abjad import *


def test_Meter_profile_nonbinary_01( ):
   t = RigidMeasure((5, 7), [
      Tuplet((4, 7), Note(0, (1, 4)) * 5)])
   assert repr(t.meter.forced) == 'Meter(5, 7)'
   assert str(t.meter.forced) == '5/7'
   assert t.meter.forced == metertools.Meter(5, 7)
   assert t.meter.forced.numerator == 5
   assert t.meter.forced.denominator == 7
   assert t.meter.forced.duration == Rational(5, 7)


def test_Meter_profile_nonbinary_02( ):
   t = RigidMeasure((6, 7), [
      Tuplet((4, 7), Note(0, (1, 4)) * 6)])
   assert repr(t.meter.forced) == 'Meter(6, 7)'
   assert str(t.meter.forced) == '6/7'
   assert t.meter.forced == metertools.Meter(6, 7)
   assert t.meter.forced.numerator == 6
   assert t.meter.forced.denominator == 7
   assert t.meter.forced.duration == Rational(6, 7)
