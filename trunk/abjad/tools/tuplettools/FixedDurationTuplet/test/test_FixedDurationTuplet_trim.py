# -*- encoding: utf-8 -*-
from abjad import *
from py.test import raises


def test_FixedDurationTuplet_trim_01():
    r'''1-element index.
    '''
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(t.select_leaves()):
        leaf.written_pitch = i
    t.trim(0)
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch == 1
    assert t[1].written_pitch.numbered_chromatic_pitch == 2


def test_FixedDurationTuplet_trim_02():
    r'''1-element index.
    '''
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(t.select_leaves()):
        leaf.written_pitch = i
    t.trim(1)
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch == 0
    assert t[1].written_pitch.numbered_chromatic_pitch == 2


def test_FixedDurationTuplet_trim_03():
    r'''1-element index.
    '''
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(t.select_leaves()):
        leaf.written_pitch = i
    t.trim(2)
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch == 0
    assert t[1].written_pitch.numbered_chromatic_pitch == 1


def test_FixedDurationTuplet_trim_04():
    r'''Raises IndexError.
    '''
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(t.select_leaves()):
        leaf.written_pitch = i
    assert raises(IndexError, 't.trim(3)')


def test_FixedDurationTuplet_trim_05():
    r'''0-element slice.
    '''
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(t.select_leaves()):
        leaf.written_pitch = i
    t.trim(0, 0)
    assert len(t) == 3
    assert t[0].written_pitch.numbered_chromatic_pitch == 0
    assert t[1].written_pitch.numbered_chromatic_pitch == 1
    assert t[2].written_pitch.numbered_chromatic_pitch == 2


def test_FixedDurationTuplet_trim_06():
    r'''1-element slice.
    '''
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(t.select_leaves()):
        leaf.written_pitch = i
    t.trim(0, 1)
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch == 1
    assert t[1].written_pitch.numbered_chromatic_pitch == 2


def test_FixedDurationTuplet_trim_07():
    r'''1-element slice.
    '''
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(t.select_leaves()):
        leaf.written_pitch = i
    t.trim(1, 2)
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch == 0
    assert t[1].written_pitch.numbered_chromatic_pitch == 2


def test_FixedDurationTuplet_trim_08():
    r'''1-element slice.
    '''
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(t.select_leaves()):
        leaf.written_pitch = i
    t.trim(2, 3)
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch == 0
    assert t[1].written_pitch.numbered_chromatic_pitch == 1


def test_FixedDurationTuplet_trim_09():
    r'''Trimming all leaves raises an exception.
    '''
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), Note(0, (1, 8)) * 3)
    for i, leaf in enumerate(t.select_leaves()):
        leaf.written_pitch = i
    raises(AssertionError, 't.trim(0, 100)')
