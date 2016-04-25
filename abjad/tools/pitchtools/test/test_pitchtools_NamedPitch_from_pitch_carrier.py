# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_NamedPitch_from_pitch_carrier_01():

    pitch = NamedPitch('df', 5)
    named_pitch = NamedPitch.from_pitch_carrier(pitch)

    assert named_pitch == NamedPitch('df', 5)


def test_pitchtools_NamedPitch_from_pitch_carrier_02():

    note = Note(('df', 5), (1, 4))
    named_pitch = NamedPitch.from_pitch_carrier(note)

    assert named_pitch == NamedPitch('df', 5)


def test_pitchtools_NamedPitch_from_pitch_carrier_03():

    note = Note(('df', 5), (1, 4))
    named_pitch = NamedPitch.from_pitch_carrier(note.note_head)

    assert named_pitch == NamedPitch('df', 5)


def test_pitchtools_NamedPitch_from_pitch_carrier_04():

    chord = Chord([('df', 5)], (1, 4))
    named_pitch = NamedPitch.from_pitch_carrier(chord)

    assert named_pitch == NamedPitch('df', 5)


def test_pitchtools_NamedPitch_from_pitch_carrier_05():

    note = Note(None, (1, 4))
    statement = 't = NamedPitch.from_pitch_carrier(note)'
    assert pytest.raises(Exception, statement)


def test_pitchtools_NamedPitch_from_pitch_carrier_06():

    chord = Chord([], (1, 4))
    statement = 't = NamedPitch.from_pitch_carrier(chord)'
    assert pytest.raises(Exception, statement)


def test_pitchtools_NamedPitch_from_pitch_carrier_07():

    chord = Chord([0, 2, 11], (1, 4))
    statement = 't = NamedPitch.from_pitch_carrier(chord)'
    assert pytest.raises(Exception, statement)


def test_pitchtools_NamedPitch_from_pitch_carrier_08():

    pitch = NamedPitch.from_pitch_carrier(13)

    assert pitch == NamedPitch(13)
