from abjad import *


def test__LeafDurationInterface_multiplied_01( ):
   '''Mulplied leaf duration == written * multiplier.'''
   t = Note(0, (1, 4))
   t.duration.multiplier = Fraction(1, 2)
   assert t.duration.multiplied == Fraction(1, 8)


def test__LeafDurationInterface_multiplied_02( ):
   '''Mulplied leaf duration == written,
      when multiplier is None.'''
   t = Note(0, (1, 4))
   assert t.duration.multiplied == Fraction(1, 4)


def test__LeafDurationInterface_multiplied_03( ):
   '''Mulplied leaf duration can be set and then unset.'''
   t = Note(0, (1, 4))
   leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
      t, Fraction(3, 8))
   assert t.duration.written == Fraction(3, 8)
   assert t.duration.multiplier == Fraction(2, 3)
   assert t.duration.multiplied == Fraction(1, 4)
   leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
      t, Fraction(1, 4))
   assert t.duration.written == Fraction(1, 4)
   assert t.duration.multiplier is None
   assert t.duration.multiplied == Fraction(1, 4)
