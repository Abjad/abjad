# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_NoteHead_written_pitch_01():
    r'''Set Note head pitch with integer.
    '''

    note = Note(13, (1, 4))
    note.note_head.written_pitch = 14

    "NoteHead(d'')"

    assert format(note.note_head) == "d''"
    assert note.note_head.written_pitch.numbered_pitch._pitch_number == 14


def test_scoretools_NoteHead_written_pitch_02():
    r'''Set Note head pitch with pitch.
    '''

    note = Note(13, (1, 4))
    note.note_head.written_pitch = NamedPitch(14)

    "NoteHead(d'')"

    assert format(note.note_head) == "d''"
    assert note.note_head.written_pitch.numbered_pitch._pitch_number == 14


def test_scoretools_NoteHead_written_pitch_03():
    r'''Can not set note head pitch to none.
    '''

    note = Note(13, (1, 4))

    assert pytest.raises(Exception, 'note.note_head.written_pitch = None')


def test_scoretools_NoteHead_written_pitch_04():
    r'''Set note head pitch from another note or note head.
    Make sure this does not cause reference problems.
    '''

    n1 = Note(12, (1, 4))
    n2 = Note(14, (1, 4))
    n1.written_pitch = n2.written_pitch

    assert n1.written_pitch == NamedPitch(14)
    assert n2.written_pitch == NamedPitch(14)
    assert n1.written_pitch is not n2.written_pitch
