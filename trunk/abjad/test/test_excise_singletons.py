from abjad import *


def test_excise_singletons_01( ):
   '''Singly-nested singleton.'''
   t = FixedDurationTuplet((2, 4), [
      Note(0, (1, 4)),
      Note(0, (1, 4)),
      FixedDurationTuplet((1, 4), [Note(0, (1, 4))])])
   excise(t.leaves[-1])
   assert isinstance(t, FixedDurationTuplet)
   assert len(t) == 2
   assert t.duration == Rational(2, 6)
   assert t.duration.multiplier == Rational(2, 3)
   assert t.duration.prolated == Rational(2, 6)
   assert isinstance(t[0], Note)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 6)


def test_excise_singletons_02( ):
   '''Doubly-nested singleton.'''
   t = FixedDurationTuplet((2, 4), [
      Note(0, (1, 4)),
      Note(0, (1, 4)),
      FixedDurationTuplet((1, 4), [
         FixedDurationTuplet((1, 4), [Note(0, (1, 4))])])])
   excise(t.leaves[-1])
   assert isinstance(t, FixedDurationTuplet)
   assert len(t) == 2
   assert t.duration == Rational(2, 6)
   assert t.duration.multiplier == Rational(2, 3)
   assert t.duration.prolated == Rational(2, 6)
   assert isinstance(t[0], Note)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 6)


def test_excise_singletons_03( ):
   '''Doubly-nested singleton.'''
   t = FixedDurationTuplet((2, 4), [
      Note(0, (1, 4)),
      Note(0, (1, 4)),
      FixedDurationTuplet((1, 4), [
         FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 2)])])
   '''
   \times 2/3 {
        c'4
        cs'4
                        d'8
                        ef'8
   }
   '''
   excise(t.leaves[-1])
   assert isinstance(t, FixedDurationTuplet)
   assert len(t) == 3
   assert t.duration == Rational(5, 12)
   assert t.duration.prolated == Rational(5, 12)
   assert t.duration.multiplier == Rational(2, 3)
   assert isinstance(t[0], Note)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 6)
   tuplet = t[-1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 1
   assert tuplet.duration == Rational(1, 8)
   assert tuplet.duration.prolated == Rational(1, 12)
   assert tuplet.duration.multiplier == Rational(1, 1)
   tuplet = t[-1][0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 1
   assert tuplet.duration == Rational(1, 8)
   assert tuplet.duration.prolated == Rational(1, 12)
   assert tuplet.duration.multiplier == Rational(1, 1)
   note = t.leaves[-1]
   assert isinstance(note, Note)
   assert note.duration == Rational(1, 8)
   assert note.duration.prolated == Rational(1, 12)
   '''
   \times 2/3 {
           c'4
           cs'4
                           d'8
   }
   '''

