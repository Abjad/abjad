# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_pitchtools_get_numbered_chromatic_pitch_class_from_pitch_carrier_01():
    r'''Works on notes.
    '''

    note = Note(13, (1, 4))
    assert pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier(note) == pitchtools.NumberedPitchClass(1)


def test_pitchtools_get_numbered_chromatic_pitch_class_from_pitch_carrier_02():
    r'''Works on one-note chords.
    '''

    chord = Chord([13], (1, 4))
    assert pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier(chord) == pitchtools.NumberedPitchClass(1)


def test_pitchtools_get_numbered_chromatic_pitch_class_from_pitch_carrier_03():
    r'''Raises exception on empty chord.
    '''

    chord = Chord([], (1, 4))
    assert py.test.raises(MissingPitchError,
        'pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier(chord)')


def test_pitchtools_get_numbered_chromatic_pitch_class_from_pitch_carrier_04():
    r'''Raises exception on multiple-note chord.
    '''

    chord = Chord([13, 14, 15], (1, 4))
    assert py.test.raises(ExtraPitchError,
        'pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier(chord)')
