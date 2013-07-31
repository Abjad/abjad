# -*- encoding: utf-8 -*-
from abjad import *


def test_notetools_make_percussion_note_01():
    r'''tied total_duration < max_note_duration.
    '''

    t = notetools.make_percussion_note(1, (5, 64), (1, 1))

    assert len(t) == 2
    assert t[0].written_pitch.numbered_chromatic_pitch == 1
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert t[0].written_duration == Duration(1, 16)
    assert t[1].written_duration == Duration(1, 64)
    assert all(len(x.select_tie_chain()) == 1 for x in t)


def test_notetools_make_percussion_note_02():
    r'''max_note_duration < tied total_duration.
    '''

    t = notetools.make_percussion_note(1, (5, 64), (1, 64))

    assert len(t) == 2
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert t[0].written_duration == Duration(1, 64)
    assert t[1].written_duration == Duration(1, 16)
    assert all(len(x.select_tie_chain()) == 1 for x in t)


def test_notetools_make_percussion_note_03():
    r'''non-tied total_duration < max_note_duration.
    '''

    t = notetools.make_percussion_note(1, (3, 64), (1, 1))

    assert len(t) == 1
    assert isinstance(t[0], Note)
    assert t[0].written_duration == Duration(3, 64)


def test_notetools_make_percussion_note_04():
    r'''max_note_duration < non-tied total_duration.
    '''

    t = notetools.make_percussion_note(1, (3, 64), (1, 64))

    assert len(t) == 2
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert t[0].written_duration == Duration(1, 64)
    assert t[1].written_duration == Duration(1, 32)
    assert all(len(x.select_tie_chain()) == 1 for x in t)
