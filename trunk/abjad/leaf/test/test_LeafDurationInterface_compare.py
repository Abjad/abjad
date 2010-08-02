from abjad import *


def test_leaf_duration_interface_compare_01( ):
   '''Written Durations can be evaluated for equality with Rationals.'''
   t = Note(0, (1, 4))
   assert t.duration.written == Rational(1, 4)


def test_leaf_duration_interface_compare_02( ):
   '''Written Durations can be evaluated for equality with integers.'''
   t = Note(0, 1)
   assert t.duration.written == 1


def test_leaf_duration_interface_compare_03( ):
   '''Written Durations can NOT be evaluated for equality with tuples.'''
   t = Note(0, (1, 4))
   assert t.duration.written == Rational(1, 4)
   assert t.duration.written != (1, 4)
   assert t.duration.written != 'foo'


def test_leaf_duration_interface_compare_04( ):
   '''Multiplier Durations can be evaluated for equality with Rationals.'''
   t = Note(1, (1, 4))
   t.duration.multiplier = Rational(1, 4)
   assert t.duration.multiplier == Rational(1, 4)


def test_leaf_duration_interface_compare_05( ):
   '''Multiplier Durations can be evaluated for equality with integers.'''
   t = Note(1, 4)
   t.duration.multiplier = Rational(1)
   assert t.duration.multiplier == Rational(1)
   assert t.duration.multiplier == 1
   assert t.duration.multiplier != (1, 1)
   assert t.duration.multiplier != 'foo'


def test_leaf_duration_interface_compare_06( ):
   '''Multiplier durations compare unequally with 
      all values other than Rationals.'''
   t = Note(0, (1, 4))
   t.duration.multiplier = Rational(1, 8)
   assert t.duration.multiplier == Rational(1, 8)
   assert t.duration.multiplier != (1, 8)
   assert t.duration.multiplier != 'foo'
