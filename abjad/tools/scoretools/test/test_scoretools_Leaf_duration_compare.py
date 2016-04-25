# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Leaf_duration_compare_01():
    r'''Written durations can be evaluated for equality with durations.
    '''

    note = Note("c'4")
    assert note.written_duration == Duration(1, 4)


def test_scoretools_Leaf_duration_compare_02():
    r'''Written durations can be evaluated for equality with integers.
    '''

    note = Note(0, 1)
    assert note.written_duration == 1


def test_scoretools_Leaf_duration_compare_03():
    r'''Written durations can NOT be evaluated for equality with tuples.
    '''

    note = Note("c'4")
    assert note.written_duration == Duration(1, 4)
    assert note.written_duration != (1, 4)
    assert note.written_duration != 'foo'
