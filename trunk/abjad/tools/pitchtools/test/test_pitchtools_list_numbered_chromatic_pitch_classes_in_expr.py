from abjad import *


def test_pitchtools_list_numbered_chromatic_pitch_classes_in_expr_01():
    '''Works with notes.'''

    note = Note(13, (1, 4))
    assert pitchtools.list_numbered_chromatic_pitch_classes_in_expr(note) == (pitchtools.NumberedChromaticPitchClass(1), )


def test_pitchtools_list_numbered_chromatic_pitch_classes_in_expr_02():
    '''Works with multiple-note chords.'''

    chord = Chord([13, 14, 15], (1, 4))
    assert pitchtools.list_numbered_chromatic_pitch_classes_in_expr(chord) == (
        pitchtools.NumberedChromaticPitchClass(1),
        pitchtools.NumberedChromaticPitchClass(2),
        pitchtools.NumberedChromaticPitchClass(3))


def test_pitchtools_list_numbered_chromatic_pitch_classes_in_expr_03():
    '''Works with one-note chords.'''

    chord = Chord([13], (1, 4))
    assert pitchtools.list_numbered_chromatic_pitch_classes_in_expr(chord) == (pitchtools.NumberedChromaticPitchClass(1), )


def test_pitchtools_list_numbered_chromatic_pitch_classes_in_expr_04():
    '''Works with empty chords.'''

    chord = Chord([], (1, 4))
    assert pitchtools.list_numbered_chromatic_pitch_classes_in_expr(chord) == ()
