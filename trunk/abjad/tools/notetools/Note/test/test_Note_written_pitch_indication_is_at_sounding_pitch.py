from abjad import *
import py.test


def test_Note_written_pitch_indication_is_at_sounding_pitch_01():

    note = Note("c'4")

    assert note.written_pitch_indication_is_at_sounding_pitch


def test_Note_written_pitch_indication_is_at_sounding_pitch_02():

    note = Note("c'4")
    note.written_pitch_indication_is_at_sounding_pitch = False

    assert not note.written_pitch_indication_is_at_sounding_pitch


def test_Note_written_pitch_indication_is_at_sounding_pitch_03():

    note = Note("c'4")

    assert py.test.raises(TypeError, "note.written_pitch_indication_is_at_sounding_pitch = 'foo'")
