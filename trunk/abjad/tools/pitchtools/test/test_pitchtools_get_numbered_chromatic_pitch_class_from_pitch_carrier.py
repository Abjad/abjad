from abjad import *
import py.test


def test_pitchtools_get_numbered_chromatic_pitch_class_from_pitch_carrier_01():
    '''Works on notes.'''

    note = Note(13, (1, 4))
    assert pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier(note) == pitchtools.NumberedChromaticPitchClass(1)


def test_pitchtools_get_numbered_chromatic_pitch_class_from_pitch_carrier_02():
    '''Works on one-note chords.'''

    chord = Chord([13], (1, 4))
    assert pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier(chord) == pitchtools.NumberedChromaticPitchClass(1)


def test_pitchtools_get_numbered_chromatic_pitch_class_from_pitch_carrier_03():
    '''Raises exception on empty chord.'''

    chord = Chord([], (1, 4))
    assert py.test.raises(MissingPitchError,
        'pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier(chord)')


def test_pitchtools_get_numbered_chromatic_pitch_class_from_pitch_carrier_04():
    '''Raises exception on multiple-note chord.'''

    chord = Chord([13, 14, 15], (1, 4))
    assert py.test.raises(ExtraPitchError,
        'pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier(chord)')
