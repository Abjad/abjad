from abjad import *


def test_measure_duration_interface_01( ):
   '''Works with no meter.'''
   t = Measure(None, Note(0, (1, 4)) * 4)
   assert t.duration == Rational(4, 4)


def test_measure_duration_interface_02( ):
   '''Works with binary meters.'''
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   assert t.duration == Rational(4, 4)


def test_measure_duration_interface_03( ):
   '''Works with nonbinary meters.'''
   t = Measure((4, 5), Note(0, (1, 4)) * 4)
   assert t.duration == Rational(4, 5)


def test_measure_duration_interface_04( ):
   '''Works with empty measures.'''
   t = Measure((4, 4), [ ])
   #assert t.duration == Rational(0)
   assert t.duration == Rational(1)


def test_measure_duration_interface_05( ):
   '''Works with mixed notes and tuplets.'''
   t = Measure((4, 4), [
      Note(0, (1, 4)), Note(0, (1, 4)), 
      FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3)])
   assert t.duration == Rational(4, 4)


def test_measure_duration_interface_06( ):
   '''Works with mixed notes and multiply nested tuplets.'''
   t = Measure((4, 4), [
      Note(0, (1, 4)), Note(0, (1, 4)), 
      FixedDurationTuplet((2, 4), [
         Note(0, (1, 8)), Note(0, (1, 8)),
         FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3)])])
   assert t.duration == Rational(4, 4)
