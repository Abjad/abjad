from abjad import *
import py.test


def test_Note_written_pitch_indication_is_nonsemantic_01():

    note = Note("c'4")

    assert not note.written_pitch_indication_is_nonsemantic


def test_Note_written_pitch_indication_is_nonsemantic_02():

    note = Note("c'4")
    note.written_pitch_indication_is_nonsemantic = True

    assert note.written_pitch_indication_is_nonsemantic
    assert not note.written_pitch_indication_is_at_sounding_pitch


def test_Note_written_pitch_indication_is_nonsemantic_03():

    note = Note("c'4")

    assert py.test.raises(TypeError, "note.written_pitch_indication_is_nonsemantic = 'foo'")
