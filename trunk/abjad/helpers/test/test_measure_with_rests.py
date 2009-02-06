from abjad import *
from py.test import raises


def test_measure_with_rests_01( ):
   '''Works with binary numerator and binary denominator.'''
   measure = measure_with_rests((4, 4))
   assert measure.meter.effective == Meter(4, 4)
   assert len(measure) == 1
   assert isinstance(measure[0], Rest)
   assert measure[0].duration.written == Rational(1, 1)
   

def test_measure_with_rests_02( ):
   '''Works with nonbinary numerator and binary denominator.'''
   measure = measure_with_rests((5, 4))
   assert measure.meter.effective == Meter(5, 4)
   assert len(measure) == 2
   assert isinstance(measure[0], Rest)
   assert isinstance(measure[1], Rest)
   assert measure[0].duration.written == Rational(1, 1)
   assert measure[1].duration.written == Rational(1, 4)
   

def test_measure_with_rests_03( ):
   '''Doesn't work with nonbinary denominator;
      TODO -- make work with nonbinary denominator.'''
   assert raises(AssignabilityError, 'measure_with_rests((4, 5))')
