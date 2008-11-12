from abjad import *
from py.test import raises

### __eq__ ###

def test_eq_01( ):
   '''Written Durations can be evaluated for equality with Rationals.'''
   t = Note(1, (1, 4))
   assert t.duration.written == Rational(1, 4)

def test_eq_02( ):
   '''Written Durations can be evaluated for equality with integers.'''
   t = Note(1, 1)
   assert t.duration.written == 1

def test_eq_03( ):
   '''Written Durations can NOT be evaluated for equality with tuples.'''
   t = Note(1, (1, 4))
   assert t.duration.written != (1, 4)


def test_eq_04( ):
   '''Multiplier Durations can be evaluated for equality with Rationals.'''
   t = Note(1, (1, 4))
   t.duration.multiplier = Rational(1, 4)
   assert t.duration.multiplier == Rational(1, 4)

def test_eq_05( ):
   '''Multiplier Durations can be evaluated for equality with integers.'''
   t = Note(1, 4)
   t.duration.multiplier = Rational(1, 1)
   assert t.duration.multiplier == 1

def test_eq_06( ):
   '''Multiplier Durations can NOT be evaluated for equality with tuples.'''
   t = Note(1, (1, 4))
   t.duration.multiplier = Rational(1, 8)
   assert t.duration.multiplier != (1, 8)

### ASSIGNMENT ###

def test_assign_01( ):
   '''Written duration can be assigned a Rational.'''
   t = Note(1, (1, 4))
   t.duration.written = Rational(1, 8)
   assert t.duration.written == Rational(1, 8)

def test_assign_02( ):
   '''Written duration can be assigned an int.'''
   t = Note(1, (1, 4))
   t.duration.written = 2
   assert t.duration.written == Rational(2, 1)

def test_assign_03( ):
   '''Written duration can NOT be assigned an tuple.'''
   t = Note(1, (1, 4))
   raises(ValueError, 't.duration.written = (1, 2)')

def test_assign_04( ):
   '''Multiplier duration can be assigned a Rational.'''
   t = Note(1, (1, 4))
   t.duration.multiplier = Rational(1, 8)
   assert t.duration.multiplier == Rational(1, 8)

def test_assign_05( ):
   '''Multiplier duration can be assigned an int.'''
   t = Note(1, (1, 4))
   t.duration.multiplier = 2
   assert t.duration.multiplier == Rational(2, 1)

def test_assign_06( ):
   '''Multiplier duration can NOT be assigned an tuple.'''
   t = Note(1, (1, 4))
   raises(ValueError, 't.duration.multiplier = (1, 2)')


### MAXIMUM WRITTED DURATION ###

def test_durations_gt_one_01( ):
   '''Leaf durations can go up to 'maxima...': duration < (16, 1) '''
   t = Note(1, 2)
   assert t.format == "cs'\\breve"
   #t.duration = 3
   t.duration.written = Rational(3)
   assert t.format == "cs'\\breve."
   #t.duration = 4
   t.duration.written = Rational(4)
   assert t.format == "cs'\\longa"
   #t.duration = 6
   t.duration.written = Rational(6)
   assert t.format == "cs'\\longa."
   #t.duration = 7
   t.duration.written = Rational(7)
   assert t.format == "cs'\\longa.."
   #t.duration = 8
   t.duration.written = Rational(8)
   assert t.format == "cs'\\maxima"
   #t.duration = 12
   t.duration.written = Rational(12)
   assert t.format == "cs'\\maxima."
   #t.duration = 14
   t.duration.written = Rational(14)
   assert t.format == "cs'\\maxima.."
   #t.duration = 15
   t.duration.written = Rational(15)
   assert t.format == "cs'\\maxima..."
   assert raises(ValueError, 'Note(1, 16)')
