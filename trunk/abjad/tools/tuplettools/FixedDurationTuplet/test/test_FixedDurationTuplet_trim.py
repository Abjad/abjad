# -*- encoding: utf-8 -*-
from abjad import *
from py.test import raises


def test_FixedDurationTuplet_trim_01():
    r'''1-element index.
    '''
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(tuplet.select_leaves()):
        leaf.written_pitch = i
    tuplet.trim(0)
    assert len(tuplet) == 2
    assert tuplet[0].written_pitch.numbered_chromatic_pitch == 1
    assert tuplet[1].written_pitch.numbered_chromatic_pitch == 2


def test_FixedDurationTuplet_trim_02():
    r'''1-element index.
    '''
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(tuplet.select_leaves()):
        leaf.written_pitch = i
    tuplet.trim(1)
    assert len(tuplet) == 2
    assert tuplet[0].written_pitch.numbered_chromatic_pitch == 0
    assert tuplet[1].written_pitch.numbered_chromatic_pitch == 2


def test_FixedDurationTuplet_trim_03():
    r'''1-element index.
    '''
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(tuplet.select_leaves()):
        leaf.written_pitch = i
    tuplet.trim(2)
    assert len(tuplet) == 2
    assert tuplet[0].written_pitch.numbered_chromatic_pitch == 0
    assert tuplet[1].written_pitch.numbered_chromatic_pitch == 1


def test_FixedDurationTuplet_trim_04():
    r'''Raises IndexError.
    '''
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(tuplet.select_leaves()):
        leaf.written_pitch = i
    assert raises(IndexError, 'tuplet.trim(3)')


def test_FixedDurationTuplet_trim_05():
    r'''0-element slice.
    '''
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(tuplet.select_leaves()):
        leaf.written_pitch = i
    tuplet.trim(0, 0)
    assert len(tuplet) == 3
    assert tuplet[0].written_pitch.numbered_chromatic_pitch == 0
    assert tuplet[1].written_pitch.numbered_chromatic_pitch == 1
    assert tuplet[2].written_pitch.numbered_chromatic_pitch == 2


def test_FixedDurationTuplet_trim_06():
    r'''1-element slice.
    '''
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(tuplet.select_leaves()):
        leaf.written_pitch = i
    tuplet.trim(0, 1)
    assert len(tuplet) == 2
    assert tuplet[0].written_pitch.numbered_chromatic_pitch == 1
    assert tuplet[1].written_pitch.numbered_chromatic_pitch == 2


def test_FixedDurationTuplet_trim_07():
    r'''1-element slice.
    '''
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(tuplet.select_leaves()):
        leaf.written_pitch = i
    tuplet.trim(1, 2)
    assert len(tuplet) == 2
    assert tuplet[0].written_pitch.numbered_chromatic_pitch == 0
    assert tuplet[1].written_pitch.numbered_chromatic_pitch == 2


def test_FixedDurationTuplet_trim_08():
    r'''1-element slice.
    '''
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(tuplet.select_leaves()):
        leaf.written_pitch = i
    tuplet.trim(2, 3)
    assert len(tuplet) == 2
    assert tuplet[0].written_pitch.numbered_chromatic_pitch == 0
    assert tuplet[1].written_pitch.numbered_chromatic_pitch == 1


def test_FixedDurationTuplet_trim_09():
    r'''Trimming all leaves raises an exception.
    '''
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(tuplet.select_leaves()):
        leaf.written_pitch = i
    raises(AssertionError, 'tuplet.trim(0, 100)')
