from abjad import *


def test__LeafDurationInterface_multiplied_01( ):
   '''Mulplied leaf duration == written * multiplier.'''
   t = Note("c'4")
   t.duration.multiplier = Duration(1, 2)
   assert t.duration.multiplied == Duration(1, 8)


def test__LeafDurationInterface_multiplied_02( ):
   '''Mulplied leaf duration == written,
      when multiplier is None.'''
   t = Note("c'4")
   assert t.duration.multiplied == Duration(1, 4)


def test__LeafDurationInterface_multiplied_03( ):
   '''Mulplied leaf duration can be set and then unset.'''
   t = Note("c'4")
   leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
      t, Duration(3, 8))
   assert t.duration.written == Duration(3, 8)
   assert t.duration.multiplier == Duration(2, 3)
   assert t.duration.multiplied == Duration(1, 4)
   leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
      t, Duration(1, 4))
   assert t.duration.written == Duration(1, 4)
   assert t.duration.multiplier is None
   assert t.duration.multiplied == Duration(1, 4)
