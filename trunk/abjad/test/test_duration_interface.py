from abjad import *

def test_eq_01( ):
   '''Durations can be evaluated for equality with Rationals.'''
   t = Note(1, (1, 4))
   assert t.duration == Rational(1, 4)

def test_eq_02( ):
   '''Durations can be evaluated for equality with tuples.'''
   t = Note(1, (1, 4))
   assert t.duration == (1, 4)

def test_eq_03( ):
   '''Durations can be evaluated for equality with integers.'''
   t = Note(1, 1)
   assert t.duration == 1


