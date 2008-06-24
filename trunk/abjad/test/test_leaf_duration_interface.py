from abjad import *
from py.test import raises

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


def test_durations_gt_one_01( ):
   '''Leaf durations can go up to 'maxima...': duration < (16, 1) '''
   t = Note(1, 2)
   assert t.format == "cs'\\breve"
   t.duration = 3
   assert t.format == "cs'\\breve."
   t.duration = 4
   assert t.format == "cs'\\longa"
   t.duration = 6
   assert t.format == "cs'\\longa."
   t.duration = 7
   assert t.format == "cs'\\longa.."
   t.duration = 8
   assert t.format == "cs'\\maxima"
   t.duration = 12
   assert t.format == "cs'\\maxima."
   t.duration = 14
   assert t.format == "cs'\\maxima.."
   t.duration = 15
   assert t.format == "cs'\\maxima..."
   assert raises(ValueError, 'Note(1, 16)')

