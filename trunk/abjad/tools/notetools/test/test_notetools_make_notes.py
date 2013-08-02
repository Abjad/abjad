# -*- encoding: utf-8 -*-
from abjad import *


def test_notetools_make_notes_01():
    r'''Can take a single pitch and a single duration.
    '''

    t = notetools.make_notes(1, (1,4))
    assert isinstance(t, list)
    assert len(t) == 1
    assert isinstance(t[0], Note)
    assert t[0].written_duration == Duration(1, 4)
    assert all(len(x.select_tie_chain()) == 1 for x in t)


def test_notetools_make_notes_02():
    r'''Tied durations result in more than one tied note.
    '''

    t = notetools.make_notes(1, (5, 8))
    assert len(t) == 2
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Note)
    assert t[0].written_duration == Duration(4, 8)
    assert t[1].written_duration == Duration(1, 8)
    assert all(len(x.select_tie_chain()) == 2 for x in t)


def test_notetools_make_notes_03():
    r'''May take a list of pitches and a single duration.
    '''

    t = notetools.make_notes([1, 2], (1, 4))
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch == 1
    assert t[1].written_pitch.numbered_chromatic_pitch == 2


def test_notetools_make_notes_04():
    r'''May take a single pitch and a list of duration.
    '''

    t = notetools.make_notes(1, [(1, 8), (1, 4)])
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch == 1
    assert t[1].written_pitch.numbered_chromatic_pitch == 1
    assert t[0].written_duration == Duration(1, 8)
    assert t[1].written_duration == Duration(1, 4)


def test_notetools_make_notes_05():
    r'''May take a list of pitches and list of durations.
    '''

    t = notetools.make_notes([0, 1], [(1, 8), (1, 4)])
    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch == 0
    assert t[1].written_pitch.numbered_chromatic_pitch == 1
    assert t[0].written_duration == Duration(1, 8)
    assert t[1].written_duration == Duration(1, 4)


def test_notetools_make_notes_06():
    r'''Durations can be durations.
    '''

    t = notetools.make_notes(1, Duration(1, 4))
    assert len(t) == 1
    assert t[0].written_duration == Duration(1, 4)


def test_notetools_make_notes_07():
    r'''Durations can be a list of durations.
    '''

    t = notetools.make_notes(1, [Duration(1, 4)])
    assert len(t) == 1
    assert t[0].written_duration == Duration(1, 4)


def test_notetools_make_notes_08():
    r'''Decrease durations monotonically.
    '''

    t = notetools.make_notes(1, (5, 16), 
        decrease_durations_monotonically=True)
    assert len(t) == 2
    assert t[0].written_duration == Duration(4, 16)
    assert t[1].written_duration == Duration(1, 16)


def test_notetools_make_notes_09():
    r'''Increase durations monotonically.
    '''

    t = notetools.make_notes(1, (5, 16), 
        decrease_durations_monotonically=False)
    assert len(t) == 2
    assert t[0].written_duration == Duration(1, 16)
    assert t[1].written_duration == Duration(4, 16)


def test_notetools_make_notes_10():
    r'''Make non-power-of-two duration.
    '''

    t = notetools.make_notes(1, (1, 36))
    assert len(t) == 1
    assert isinstance(t[0], Tuplet)
    assert len(t[0]) == 1
    assert t[0].get_duration() == Duration(1, 36)
    assert t[0][0].get_duration() == Duration(1, 36)
    assert t[0][0].written_duration == Duration(1, 32)


def test_notetools_make_notes_11():
    r'''Make multiple non-power-or-two durations.
    '''

    t = notetools.make_notes(1, [(1, 12), (1, 6), (1, 8)])

    r'''
    \times 2/3 {
        cs'8
        cs'4
    }
    cs'8
    '''

    assert len(t) == 2
    assert isinstance(t[0], Tuplet)
    assert isinstance(t[1], Note)
    assert len(t[0]) == 2
    assert t[0].get_duration() == Duration(3, 12)
    assert t[0][0].get_duration() == Duration(1, 12)
    assert t[0][1].get_duration() == Duration(1, 6)
    assert t[0][0].written_duration == Duration(1, 8)
    assert t[0][1].written_duration == Duration(1, 4)
    assert t[1].written_duration == Duration(1, 8)


def test_notetools_make_notes_12():

    t = notetools.make_notes(1, [(5, 12), (1, 6), (1, 8)], 
        decrease_durations_monotonically=False)
    assert len(t) == 2
    assert isinstance(t[0], Tuplet)
    assert isinstance(t[1], Note)
    assert len(t[0]) == 3
    assert t[0].get_duration() == Duration(7, 12)
    assert t[0][0].get_duration() == Duration(1, 12)
    assert t[0][1].get_duration() == Duration(4, 12)
    assert t[0][2].get_duration() == Duration(1, 6)
    assert t[0][0].written_duration == Duration(1, 8)
    assert t[0][1].written_duration == Duration(4, 8)
    assert t[0][2].written_duration == Duration(1, 4)
    assert t[1].written_duration == Duration(1, 8)
