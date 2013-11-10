# -*- encoding: utf-8 -*-
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


def test_scoretools_Leaf_duration_compare_04():
    r'''Multiplier durations can be evaluated for equality with durations.
    '''

    note = Note(1, (1, 4))
    note.lilypond_duration_multiplier = Multiplier(1, 4)
    assert note.lilypond_duration_multiplier == Multiplier(1, 4)


def test_scoretools_Leaf_duration_compare_05():
    r'''Multiplier durations can be evaluated for equality with integers.
    '''

    note = Note(1, 4)
    note.lilypond_duration_multiplier = Multiplier(1)
    assert note.lilypond_duration_multiplier == Multiplier(1)
    assert note.lilypond_duration_multiplier == 1
    assert note.lilypond_duration_multiplier != (1, 1)
    assert note.lilypond_duration_multiplier != 'foo'


def test_scoretools_Leaf_duration_compare_06():
    r'''Multiplier durations compare unequally with
    all values other than durations.
    '''

    note = Note("c'4")
    note.lilypond_duration_multiplier = Multiplier(1, 8)
    assert note.lilypond_duration_multiplier == Multiplier(1, 8)
    assert note.lilypond_duration_multiplier != (1, 8)
    assert note.lilypond_duration_multiplier != 'foo'
