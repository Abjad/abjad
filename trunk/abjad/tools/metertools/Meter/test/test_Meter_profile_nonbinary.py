from abjad import *


def test_Meter_profile_nonbinary_01( ):
   t = Measure((5, 7), [
      Tuplet((4, 7), Note(0, (1, 4)) * 5)])
   #assert repr(t.meter.forced) == 'Meter(5, 7)'
   #assert str(t.meter.forced) == '5/7'
   assert t.meter.effective == marktools.TimeSignatureMark(5, 7)
   assert t.meter.effective.numerator == 5
   assert t.meter.effective.denominator == 7
   assert t.meter.effective.duration == Rational(5, 7)


def test_Meter_profile_nonbinary_02( ):
   t = Measure((6, 7), [
      Tuplet((4, 7), Note(0, (1, 4)) * 6)])
   #assert repr(t.meter.forced) == 'Meter(6, 7)'
   #assert str(t.meter.forced) == '6/7'
   assert t.meter.effective == marktools.TimeSignatureMark(6, 7)
   assert t.meter.effective.numerator == 6
   assert t.meter.effective.denominator == 7
   assert t.meter.effective.duration == Rational(6, 7)
