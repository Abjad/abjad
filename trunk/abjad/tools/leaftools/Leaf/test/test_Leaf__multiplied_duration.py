# -*- encoding: utf-8 -*-
from abjad import *


def test_Leaf__multiplied_duration_01():
    r'''Mulplied leaf duration == written * multiplier.
    '''
    note = Note("c'4")
    note.lilypond_duration_multiplier = Duration(1, 2)
    assert note._multiplied_duration == Duration(1, 8)


def test_Leaf__multiplied_duration_02():
    r'''Mulplied leaf duration == written,
        when multiplier is None.'''
    note = Note("c'4")
    assert note._multiplied_duration == Duration(1, 4)


def test_Leaf__multiplied_duration_03():
    r'''Mulplied leaf duration can be set and then unset.
    '''
    t = Note("c'4")
    leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
        t, Duration(3, 8))
    assert t.written_duration == Duration(3, 8)
    assert t.lilypond_duration_multiplier == Duration(2, 3)
    assert t._multiplied_duration == Duration(1, 4)
    leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(
        t, Duration(1, 4))
    assert t.written_duration == Duration(1, 4)
    assert t.lilypond_duration_multiplier is None
    assert t._multiplied_duration == Duration(1, 4)
