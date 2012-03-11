from abjad import *
import py.test


def test__Leaf_duration_assign_01():
    '''Written duration can be assigned a Duration.'''
    t = Note(1, (1, 4))
    t.written_duration = Duration(1, 8)
    assert t.written_duration == Duration(1, 8)


def test__Leaf_duration_assign_02():
    '''Written duration can be assigned an int.'''
    t = Note(1, (1, 4))
    t.written_duration = 2
    assert t.written_duration == Duration(2, 1)


def test__Leaf_duration_assign_03():
    '''Written duration can be assigned an tuple.'''
    t = Note(1, (1, 4))
    t.written_duration = (1, 2)
    assert t.written_duration == Duration(1, 2)


def test__Leaf_duration_assign_04():
    '''Multiplier duration can be assigned a Duration.'''
    t = Note(1, (1, 4))
    t.duration_multiplier = Duration(1, 8)
    assert t.duration_multiplier == Duration(1, 8)


def test__Leaf_duration_assign_05():
    '''Multiplier duration can be assigned an int.'''
    t = Note(1, (1, 4))
    t.duration_multiplier = 2
    assert t.duration_multiplier == Duration(2, 1)
