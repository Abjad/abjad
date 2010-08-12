from abjad import *
import py.test


def test_leaftools_make_accelerating_notes_with_lilypond_multipliers_01( ):
   '''Pitches can be a list of any length greater than 1.'''
   t = leaftools.make_accelerating_notes_with_lilypond_multipliers([1], Rational(2), Rational(1, 2), Rational(1, 2))
   assert len(t) == 4
   for n in t:
      assert n.pitch.number == 1


def test_leaftools_make_accelerating_notes_with_lilypond_multipliers_02( ):
   '''Pitches can be a list of any length greater than 1.'''
   t = leaftools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Rational(2), Rational(1, 2), Rational(1, 2))
   assert len(t) == 4
   for i, n in enumerate(t):
      if i % 2 == 0:
         assert n.pitch.number == 1
      else:
         assert n.pitch.number == 2


def test_leaftools_make_accelerating_notes_with_lilypond_multipliers_03( ):
   '''Start and stop fractions must be smaller than durations.'''
   code = 't = leaftools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Rational(2), Rational(4), Rational(1, 2))'
   assert py.test.raises(ValueError, code)


def test_leaftools_make_accelerating_notes_with_lilypond_multipliers_04( ):
   '''
   The default written duration of notes returned is 1/8.
   '''
   t = leaftools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Rational(2), Rational(1, 2), Rational(1, 2))
   for n in t:
      assert n.duration.written == Rational(1, 8)


def test_leaftools_make_accelerating_notes_with_lilypond_multipliers_05( ):
   '''
   The written duration can be set.
   '''
   t = leaftools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Rational(2), Rational(1, 2), Rational(1, 2), 
   written=Rational(1))
   for n in t:
      assert n.duration.written == Rational(1)


def test_leaftools_make_accelerating_notes_with_lilypond_multipliers_06( ):
   '''
   note_curve( ) can take an exp argument to set the exponent in 
   exponential interpolation.
   '''
   t_line = leaftools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Rational(2), Rational(1, 32), Rational(1, 8), 1)
   t_exp = leaftools.make_accelerating_notes_with_lilypond_multipliers([1, 2], Rational(2), Rational(1, 32), Rational(1, 8), 2)
   assert t_exp[4].duration.prolated < t_line[4].duration.prolated
