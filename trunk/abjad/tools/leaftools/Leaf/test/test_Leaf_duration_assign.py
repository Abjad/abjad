from abjad import *
import py.test


def test_Leaf_duration_assign_01():
    r'''Written duration can be assigned a Duration.
    '''
    t = Note(1, (1, 4))
    t.written_duration = Duration(1, 8)
    assert t.written_duration == Duration(1, 8)


def test_Leaf_duration_assign_02():
    r'''Written duration can be assigned an int.
    '''
    t = Note(1, (1, 4))
    t.written_duration = 2
    assert t.written_duration == Duration(2, 1)


def test_Leaf_duration_assign_03():
    r'''Written duration can be assigned an tuple.
    '''
    t = Note(1, (1, 4))
    t.written_duration = (1, 2)
    assert t.written_duration == Duration(1, 2)


def test_Leaf_duration_assign_04():
    r'''Multiplier duration can be assigned a Duration.
    '''
    t = Note(1, (1, 4))
    t.duration_multiplier = Duration(1, 8)
    assert t.duration_multiplier == Duration(1, 8)


def test_Leaf_duration_assign_05():
    r'''Multiplier duration can be assigned an int.
    '''
    t = Note(1, (1, 4))
    t.duration_multiplier = 2
    assert t.duration_multiplier == Duration(2, 1)
