# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_make_notes_01():
    r'''Can take a single pitch and a single duration.
    '''

    note = scoretools.make_notes(1, (1,4))
    assert isinstance(note, selectiontools.Selection)
    assert len(note) == 1
    assert isinstance(note[0], Note)
    assert note[0].written_duration == Duration(1, 4)
    assert all(len(inspect_(x).get_logical_tie()) == 1 for x in note)


def test_scoretools_make_notes_02():
    r'''Tied durations result in more than one tied note.
    '''

    note = scoretools.make_notes(1, (5, 8))
    assert len(note) == 2
    assert isinstance(note[0], Note)
    assert isinstance(note[1], Note)
    assert note[0].written_duration == Duration(4, 8)
    assert note[1].written_duration == Duration(1, 8)
    assert all(len(inspect_(x).get_logical_tie()) == 2 for x in note)


def test_scoretools_make_notes_03():
    r'''May take a list of pitches and a single duration.
    '''

    t = scoretools.make_notes([1, 2], (1, 4))
    assert len(t) == 2
    assert t[0].written_pitch.numbered_pitch == 1
    assert t[1].written_pitch.numbered_pitch == 2


def test_scoretools_make_notes_04():
    r'''May take a single pitch and a list of duration.
    '''

    may = scoretools.make_notes(1, [(1, 8), (1, 4)])
    assert len(may) == 2
    assert may[0].written_pitch.numbered_pitch == 1
    assert may[1].written_pitch.numbered_pitch == 1
    assert may[0].written_duration == Duration(1, 8)
    assert may[1].written_duration == Duration(1, 4)


def test_scoretools_make_notes_05():
    r'''May take a list of pitches and list of durations.
    '''

    duration = scoretools.make_notes([0, 1], [(1, 8), (1, 4)])
    assert len(duration) == 2
    assert duration[0].written_pitch.numbered_pitch == 0
    assert duration[1].written_pitch.numbered_pitch == 1
    assert duration[0].written_duration == Duration(1, 8)
    assert duration[1].written_duration == Duration(1, 4)


def test_scoretools_make_notes_06():
    r'''Durations can be durations.
    '''

    duration = scoretools.make_notes(1, Duration(1, 4))
    assert len(duration) == 1
    assert duration[0].written_duration == Duration(1, 4)


def test_scoretools_make_notes_07():
    r'''Durations can be a list of durations.
    '''

    duration = scoretools.make_notes(1, [Duration(1, 4)])
    assert len(duration) == 1
    assert duration[0].written_duration == Duration(1, 4)


def test_scoretools_make_notes_08():
    r'''Decrease durations monotonically.
    '''

    true = scoretools.make_notes(1, (5, 16),
        decrease_durations_monotonically=True)
    assert len(true) == 2
    assert true[0].written_duration == Duration(4, 16)
    assert true[1].written_duration == Duration(1, 16)


def test_scoretools_make_notes_09():
    r'''Increase durations monotonically.
    '''

    false = scoretools.make_notes(1, (5, 16),
        decrease_durations_monotonically=False)
    assert len(false) == 2
    assert false[0].written_duration == Duration(1, 16)
    assert false[1].written_duration == Duration(4, 16)


def test_scoretools_make_notes_10():
    r'''Make non-power-of-two duration.
    '''

    tuplet = scoretools.make_notes(1, (1, 36))
    assert len(tuplet) == 1
    assert isinstance(tuplet[0], Tuplet)
    assert len(tuplet[0]) == 1
    assert inspect_(tuplet[0]).get_duration() == Duration(1, 36)
    assert inspect_(tuplet[0][0]).get_duration() == Duration(1, 36)
    assert tuplet[0][0].written_duration == Duration(1, 32)


def test_scoretools_make_notes_11():
    r'''Make multiple non-power-or-two durations.
    '''

    tuplet = scoretools.make_notes(1, [(1, 12), (1, 6), (1, 8)])

    r'''
    \times 2/3 {
        cs'8
        cs'4
    }
    cs'8
    '''

    assert len(tuplet) == 2
    assert isinstance(tuplet[0], Tuplet)
    assert isinstance(tuplet[1], Note)
    assert len(tuplet[0]) == 2
    assert inspect_(tuplet[0]).get_duration() == Duration(3, 12)
    assert inspect_(tuplet[0][0]).get_duration() == Duration(1, 12)
    assert inspect_(tuplet[0][1]).get_duration() == Duration(1, 6)
    assert tuplet[0][0].written_duration == Duration(1, 8)
    assert tuplet[0][1].written_duration == Duration(1, 4)
    assert tuplet[1].written_duration == Duration(1, 8)


def test_scoretools_make_notes_12():

    t = scoretools.make_notes(1, [(5, 12), (1, 6), (1, 8)],
        decrease_durations_monotonically=False)
    assert len(t) == 2
    assert isinstance(t[0], Tuplet)
    assert isinstance(t[1], Note)
    assert len(t[0]) == 3
    assert inspect_(t[0]).get_duration() == Duration(7, 12)
    assert inspect_(t[0][0]).get_duration() == Duration(1, 12)
    assert inspect_(t[0][1]).get_duration() == Duration(4, 12)
    assert inspect_(t[0][2]).get_duration() == Duration(1, 6)
    assert t[0][0].written_duration == Duration(1, 8)
    assert t[0][1].written_duration == Duration(4, 8)
    assert t[0][2].written_duration == Duration(1, 4)
    assert t[1].written_duration == Duration(1, 8)
