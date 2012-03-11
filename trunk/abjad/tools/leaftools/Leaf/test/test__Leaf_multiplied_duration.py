from abjad import *


def test__Leaf_multiplied_duration_01():
    '''Mulplied leaf duration == written * multiplier.'''
    t = Note("c'4")
    t.duration_multiplier = Duration(1, 2)
    assert t.multiplied_duration == Duration(1, 8)


def test__Leaf_multiplied_duration_02():
    '''Mulplied leaf duration == written,
        when multiplier is None.'''
    t = Note("c'4")
    assert t.multiplied_duration == Duration(1, 4)


def test__Leaf_multiplied_duration_03():
    '''Mulplied leaf duration can be set and then unset.'''
    t = Note("c'4")
    leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
        t, Duration(3, 8))
    assert t.written_duration == Duration(3, 8)
    assert t.duration_multiplier == Duration(2, 3)
    assert t.multiplied_duration == Duration(1, 4)
    leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
        t, Duration(1, 4))
    assert t.written_duration == Duration(1, 4)
    assert t.duration_multiplier is None
    assert t.multiplied_duration == Duration(1, 4)
