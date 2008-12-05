from abjad import *


def test_excise_tuplet_01( ):
   '''Nested fixed-duration tuplet.'''
   t = Measure((4, 4), [
      FixedDurationTuplet((2,2), [Note(0, (1,2)), Note(1, (1,2)), 
      FixedDurationTuplet((2,4), [Note(i, (1,4)) for i in range(2, 5)])])])
   '''
   \time 4/4
   \times 2/3 {
          c'2
          cs'2
          \times 2/3 {
                  d'4
                  ef'4
                  e'4
          }
   }
   '''
   excise(t.leaves[-1])
   measure = t
   assert isinstance(measure, Measure)
   assert measure.meter == (8, 9)
   assert len(measure) == 1
   tuplet = t[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 3
   #assert tuplet.duration == Rational(1)
   assert tuplet.duration.target == Rational(1)
   assert tuplet.duration.prolated == Rational(8, 9)
   assert tuplet.duration.multiplier == Rational(3, 4)
   note = t[0][0]
   assert isinstance(note, Note)
   #assert note.duration == Rational(1, 2)
   assert note.duration.written == Rational(1, 2)
   assert note.duration.prolated == Rational(1, 3)
   tuplet = t[0][-1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 2
   #assert tuplet.duration == Rational(1, 3)
   assert tuplet.duration.target == Rational(1, 3)
   assert tuplet.duration.prolated == Rational(2, 9)
   assert tuplet.duration.multiplier == Rational(2, 3)
   note = t[0][-1][0]
   assert isinstance(note, Note)
   #assert note.duration == Rational(1, 4)
   assert note.duration.written == Rational(1, 4)
   assert note.duration.prolated == Rational(1, 9)
   '''
   \time 8/9
   \compressMusic #'(8 . 9) {
          \fraction \times 3/4 {
                  c'2
                  cs'2
                  \times 2/3 {
                          d'4
                          ef'4
                  }
          }
   }
   '''


#def test_excise_tuplet_02( ):
#   '''Nested fixed-multiplier tuplet.'''
#   t = FixedMultiplierTuplet((2,3), [Note(0, (1,2)), Note(1, (1,2)), \
#      FixedMultiplierTuplet((2,3), [Note(i, (1,4)) for i in range(2, 5)])])
#   excise(t.leaves[-1])
#   assert isinstance(t, FixedMultiplierTuplet)
#   assert len(t) == 3
#   assert t.duration == Rational(8,9)
#   assert t.duration.prolated == Rational(8,9)
#   assert isinstance(t[2], FixedMultiplierTuplet)
#   assert t[2].duration == Rational(2,6)
#   assert t[2].duration.prolated == Rational(2, 9)
