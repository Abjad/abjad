import abjad
import pytest


def test_NoteHead_written_pitch_01():
    """
    Set note-head head pitch with integer.
    """

    note = abjad.Note(13, (1, 4))
    note.note_head.written_pitch = 14

    "NoteHead(d'')"

    assert format(note.note_head) == "d''"
    assert note.note_head.written_pitch == 14


def test_NoteHead_written_pitch_02():
    """
    Set note-head pitch with pitch.
    """

    note = abjad.Note(13, (1, 4))
    note.note_head.written_pitch = abjad.NamedPitch(14)

    "NoteHead(d'')"

    assert format(note.note_head) == "d''"
    assert note.note_head.written_pitch == 14


def test_NoteHead_written_pitch_03():
    """
    Can not set note-head pitch to none.
    """

    note = abjad.Note(13, (1, 4))

    assert pytest.raises(Exception, 'note.note_head.written_pitch = None')


def test_NoteHead_written_pitch_04():
    """
    Set note-head pitch from another note or note-head.
    Make sure this does not cause reference problems.
    """

    n1 = abjad.Note(12, (1, 4))
    n2 = abjad.Note(14, (1, 4))
    n1.written_pitch = n2.written_pitch

    assert n1.written_pitch == abjad.NamedPitch(14)
    assert n2.written_pitch == abjad.NamedPitch(14)
    assert n1.written_pitch is not n2.written_pitch
