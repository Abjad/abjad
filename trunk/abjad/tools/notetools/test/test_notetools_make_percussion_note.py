# -*- encoding: utf-8 -*-
from abjad import *


def test_notetools_make_percussion_note_01():
    r'''tied total_duration < max_note_duration.
    '''

    note = notetools.make_percussion_note(1, (5, 64), (1, 1))

    assert len(note) == 2
    assert note[0].written_pitch.numbered_chromatic_pitch == 1
    assert isinstance(note[0], Note)
    assert isinstance(note[1], Rest)
    assert note[0].written_duration == Duration(1, 16)
    assert note[1].written_duration == Duration(1, 64)
    assert all(len(inspect(x).get_tie_chain()) == 1 for x in note)


def test_notetools_make_percussion_note_02():
    r'''max_note_duration < tied total_duration.
    '''

    note = notetools.make_percussion_note(1, (5, 64), (1, 64))

    assert len(note) == 2
    assert isinstance(note[0], Note)
    assert isinstance(note[1], Rest)
    assert note[0].written_duration == Duration(1, 64)
    assert note[1].written_duration == Duration(1, 16)
    assert all(len(inspect(x).get_tie_chain()) == 1 for x in note)


def test_notetools_make_percussion_note_03():
    r'''non-tied total_duration < max_note_duration.
    '''

    note = notetools.make_percussion_note(1, (3, 64), (1, 1))

    assert len(note) == 1
    assert isinstance(note[0], Note)
    assert note[0].written_duration == Duration(3, 64)


def test_notetools_make_percussion_note_04():
    r'''max_note_duration < non-tied total_duration.
    '''

    t = notetools.make_percussion_note(1, (3, 64), (1, 64))

    assert len(t) == 2
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert t[0].written_duration == Duration(1, 64)
    assert t[1].written_duration == Duration(1, 32)
    assert all(len(inspect(x).get_tie_chain()) == 1 for x in t)
