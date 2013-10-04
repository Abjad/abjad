# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_pitchtools_get_named_pitch_from_pitch_carrier_01():

    pitch = pitchtools.NamedPitch('df', 5)
    namedchromaticpitch = pitchtools.get_named_pitch_from_pitch_carrier(pitch)

    assert namedchromaticpitch == pitchtools.NamedPitch('df', 5)


def test_pitchtools_get_named_pitch_from_pitch_carrier_02():

    note = Note(('df', 5), (1, 4))
    namedchromaticpitch = pitchtools.get_named_pitch_from_pitch_carrier(note)

    assert namedchromaticpitch == pitchtools.NamedPitch('df', 5)


def test_pitchtools_get_named_pitch_from_pitch_carrier_03():

    note = Note(('df', 5), (1, 4))
    namedchromaticpitch = pitchtools.get_named_pitch_from_pitch_carrier(note.note_head)

    assert namedchromaticpitch == pitchtools.NamedPitch('df', 5)


def test_pitchtools_get_named_pitch_from_pitch_carrier_04():

    chord = Chord([('df', 5)], (1, 4))
    namedchromaticpitch = pitchtools.get_named_pitch_from_pitch_carrier(chord)

    assert namedchromaticpitch == pitchtools.NamedPitch('df', 5)


def test_pitchtools_get_named_pitch_from_pitch_carrier_05():

    note = Note(None, (1, 4))
    assert py.test.raises(
        MissingPitchError, 't = pitchtools.get_named_pitch_from_pitch_carrier(note)')


def test_pitchtools_get_named_pitch_from_pitch_carrier_06():

    chord = Chord([], (1, 4))
    assert py.test.raises(
        MissingPitchError, 't = pitchtools.get_named_pitch_from_pitch_carrier(chord)')


def test_pitchtools_get_named_pitch_from_pitch_carrier_07():

    chord = Chord([0, 2, 11], (1, 4))
    assert py.test.raises(
        ExtraPitchError, 't = pitchtools.get_named_pitch_from_pitch_carrier(chord)')


def test_pitchtools_get_named_pitch_from_pitch_carrier_08():

    pitch = pitchtools.get_named_pitch_from_pitch_carrier(13)

    assert pitch == pitchtools.NamedPitch(13)
