# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_get_numbered_pitch_class_from_pitch_carrier_01():
    r'''Works on notes.
    '''

    note = Note(13, (1, 4))
    result = pitchtools.get_numbered_pitch_class_from_pitch_carrier(note)
    assert result == pitchtools.NumberedPitchClass(1)


def test_pitchtools_get_numbered_pitch_class_from_pitch_carrier_02():
    r'''Works on one-note chords.
    '''

    chord = Chord([13], (1, 4))
    result = pitchtools.get_numbered_pitch_class_from_pitch_carrier(chord)
    assert result == pitchtools.NumberedPitchClass(1)


def test_pitchtools_get_numbered_pitch_class_from_pitch_carrier_03():
    r'''Raises exception on empty chord.
    '''

    chord = Chord([], (1, 4))
    statement = 'pitchtools.get_numbered_pitch_class_from_pitch_carrier(chord)'
    assert pytest.raises(Exception, statement)


def test_pitchtools_get_numbered_pitch_class_from_pitch_carrier_04():
    r'''Raises exception on multiple-note chord.
    '''

    chord = Chord([13, 14, 15], (1, 4))
    statement = 'pitchtools.get_numbered_pitch_class_from_pitch_carrier(chord)'
    assert pytest.raises(Exception, statement)
