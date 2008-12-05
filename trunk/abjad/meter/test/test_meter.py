from abjad import *


### TEST TYPICAL METER ###

def test_typical_meter_01( ):
   t = Measure((5, 8), Note(0, (1, 8)) * 5)
   assert repr(t.meter) == '_Meter(5, 8)'
   assert str(t.meter) == '5/8'
   assert t.meter.pair == (5, 8)
   assert t.meter.numerator == 5
   assert t.meter.denominator == 8
   assert t.meter.duration == Rational(5, 8)

def test_typical_meter_02( ):
   t = Measure((6, 8), Note(0, (1, 8)) * 6)
   assert repr(t.meter) == '_Meter(6, 8)'
   assert str(t.meter) == '6/8'
   assert t.meter.pair == (6, 8)
   assert t.meter.numerator == 6
   assert t.meter.denominator == 8
   assert t.meter.duration == Rational(6, 8)


### TEST NONBINARY METER ###

def test_nonbinary_meter_01( ):
   t = Measure((5, 7), [FixedMultiplierTuplet((4, 7), Note(0, (1, 4)) * 5)])
   assert repr(t.meter) == '_Meter(5, 7)'
   assert str(t.meter) == '5/7'
   assert t.meter.pair == (5, 7)
   assert t.meter.numerator == 5
   assert t.meter.denominator == 7
   assert t.meter.duration == Rational(5, 7)

def test_nonbinary_meter_02( ):
   t = Measure((6, 7), [FixedMultiplierTuplet((4, 7), Note(0, (1, 4)) * 6)])
   assert repr(t.meter) == '_Meter(6, 7)'
   assert str(t.meter) == '6/7'
   assert t.meter.pair == (6, 7)
   assert t.meter.numerator == 6
   assert t.meter.denominator == 7
   assert t.meter.duration == Rational(6, 7)
