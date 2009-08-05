from abjad.tools.construct import notes_curve
from abjad.rational import Rational
import py.test

def test_construct_notes_curve_01( ):
   '''Pitches can be a list of any length > 1.'''
   t = notes_curve([1], Rational(2), Rational(1, 2), Rational(1, 2))
   assert len(t) == 4
   for n in t:
      assert n.pitch.number == 1


def test_construct_notes_curve_02( ):
   '''Pitches can be a list of any length > 1.'''
   t = notes_curve([1, 2], Rational(2), Rational(1, 2), Rational(1, 2))
   assert len(t) == 4
   for i, n in enumerate(t):
      if i % 2 == 0:
         assert n.pitch.number == 1
      else:
         assert n.pitch.number == 2


def test_construct_notes_curve_03( ):
   '''Start and stop fractions must be smaller than durations.'''
   code = 't = notes_curve([1, 2], Rational(2), Rational(4), Rational(1, 2))'
   assert py.test.raises(ValueError, code)


def test_construct_notes_curve_04( ):
   '''
   The default written duration of notes returned is 1/8.
   '''
   t = notes_curve([1, 2], Rational(2), Rational(1, 2), Rational(1, 2))
   for n in t:
      assert n.duration.written == Rational(1, 8)


def test_construct_notes_curve_05( ):
   '''
   The written duration can be set.
   '''
   t = notes_curve([1, 2], Rational(2), Rational(1, 2), Rational(1, 2), 
   written=Rational(1))
   for n in t:
      assert n.duration.written == Rational(1)


def test_construct_notes_curve_06( ):
   '''
   note_curve( ) can take an exp argument to set the exponent in 
   exponential interpolation.
   '''
   t_line = notes_curve([1, 2], Rational(2), Rational(1, 32), Rational(1, 8), 1)
   t_exp = notes_curve([1, 2], Rational(2), Rational(1, 32), Rational(1, 8), 2)
   assert t_line[4].duration.prolated > t_exp[4].duration.prolated


