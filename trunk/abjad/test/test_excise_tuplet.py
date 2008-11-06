from abjad import *


def test_excise_tuplet_01(  ):
   '''Nonnested fixed-duration tuplet.'''
   t = FixedDurationTuplet((4, 4), Note(0, (1, 4)) * 5)
   excise(t.leaves[0])
   assert isinstance(t, FixedDurationTuplet)
   assert len(t) == 4
   #assert t.duration == Rational(4, 5)
   assert t.duration.target == Rational(4, 5)
   assert t.duration.prolated == Rational(4, 5)
   assert isinstance(t[0], Note)
   #assert t[0].duration == Rational(1, 4)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 5)


def test_excise_tuplet_02(  ):
   '''Nonnested fixed-multiplier tuplet.'''
   t = FixedMultiplierTuplet((4, 5), Note(0, (1, 4)) * 5)
   excise(t.leaves[0])
   assert isinstance(t, FixedMultiplierTuplet)
   assert len(t) == 4
   #assert t.duration == Rational(4, 5)
   assert t.duration.preprolated == Rational(4, 5)
   assert t.duration.prolated == Rational(4, 5)
   assert isinstance(t[0], Note)
   #assert t[0].duration == Rational(1, 4)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 5)


def test_excise_tuplet_03( ):
   '''Nested fixed-duration tuplet.'''
   t = FixedDurationTuplet((2,2), [Note(0, (1,2)), Note(1, (1,2)), \
      FixedDurationTuplet((2,4), [Note(i, (1,4)) for i in range(2, 5)])])
   excise(t.leaves[-1])
   assert isinstance(t, FixedDurationTuplet)
   assert len(t) == 3
   #assert t.duration == Rational(8,9)
   assert t.duration.target == Rational(8,9)
   assert t.duration.prolated == Rational(8,9)
   assert isinstance(t[2], FixedDurationTuplet)
   #assert t[2].duration == Rational(2,6)
   assert t[2].duration.target == Rational(2,6)
   assert t[2].duration.prolated == Rational(2, 9)


def test_excise_tuplet_04( ):
   '''Nested fixed-multiplier tuplet.'''
   t = FixedMultiplierTuplet((2,3), [Note(0, (1,2)), Note(1, (1,2)), \
      FixedMultiplierTuplet((2,3), [Note(i, (1,4)) for i in range(2, 5)])])
   excise(t.leaves[-1])
   assert isinstance(t, FixedMultiplierTuplet)
   assert len(t) == 3
   #assert t.duration == Rational(8,9)
   assert t.duration.preprolated == Rational(8,9)
   assert t.duration.prolated == Rational(8,9)
   assert isinstance(t[2], FixedMultiplierTuplet)
   #assert t[2].duration == Rational(2,6)
   assert t[2].duration.preprolated == Rational(2,6)
   assert t[2].duration.prolated == Rational(2, 9)
