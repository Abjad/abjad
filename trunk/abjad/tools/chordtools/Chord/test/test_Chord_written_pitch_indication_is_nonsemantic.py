from abjad import *
import py.test


def test_Chord_written_pitch_indication_is_nonsemantic_01():

    chord = Chord("<c' e' g'>4")
    assert not chord.written_pitch_indication_is_nonsemantic


def test_Chord_written_pitch_indication_is_nonsemantic_02():

    chord = Chord("<c' e' g'>4")
    chord.written_pitch_indication_is_nonsemantic = True

    assert chord.written_pitch_indication_is_nonsemantic
    assert not chord.written_pitch_indication_is_at_sounding_pitch


def test_Chord_written_pitch_indication_is_nonsemantic_03():

    chord = Chord("<c' e' g'>4")

    assert py.test.raises(TypeError, "chord.written_pitch_indication_is_nonsemantic = 'foo'")
