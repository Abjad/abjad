from abjad import *


def test_Leaf_duration_compare_01():
    r'''Written Durations can be evaluated for equality with Durations.
    '''
    t = Note("c'4")
    assert t.written_duration == Duration(1, 4)


def test_Leaf_duration_compare_02():
    r'''Written Durations can be evaluated for equality with integers.
    '''
    t = Note(0, 1)
    assert t.written_duration == 1


def test_Leaf_duration_compare_03():
    r'''Written Durations can NOT be evaluated for equality with tuples.
    '''
    t = Note("c'4")
    assert t.written_duration == Duration(1, 4)
    assert t.written_duration != (1, 4)
    assert t.written_duration != 'foo'


def test_Leaf_duration_compare_04():
    r'''Multiplier Durations can be evaluated for equality with Durations.
    '''
    t = Note(1, (1, 4))
    t.duration_multiplier = Duration(1, 4)
    assert t.duration_multiplier == Duration(1, 4)


def test_Leaf_duration_compare_05():
    r'''Multiplier Durations can be evaluated for equality with integers.
    '''
    t = Note(1, 4)
    t.duration_multiplier = Duration(1)
    assert t.duration_multiplier == Duration(1)
    assert t.duration_multiplier == 1
    assert t.duration_multiplier != (1, 1)
    assert t.duration_multiplier != 'foo'


def test_Leaf_duration_compare_06():
    r'''Multiplier durations compare unequally with
        all values other than Durations.'''
    t = Note("c'4")
    t.duration_multiplier = Duration(1, 8)
    assert t.duration_multiplier == Duration(1, 8)
    assert t.duration_multiplier != (1, 8)
    assert t.duration_multiplier != 'foo'
