from abjad import *


def test_pitchtools_expr_has_duplicate_numbered_chromatic_pitch_class_01():
    '''Works with chords.'''

    chord = Chord([1, 13, 14], (1, 4))
    assert pitchtools.expr_has_duplicate_numbered_chromatic_pitch_class(chord)

    chord = Chord([1, 14, 15], (1, 4))
    assert not pitchtools.expr_has_duplicate_numbered_chromatic_pitch_class(chord)


def test_pitchtools_expr_has_duplicate_numbered_chromatic_pitch_class_02():
    '''Works with notes, rests and skips.'''

    assert not pitchtools.expr_has_duplicate_numbered_chromatic_pitch_class(Note(13, (1, 4)))
    assert not pitchtools.expr_has_duplicate_numbered_chromatic_pitch_class(Rest((1, 4)))
    assert not pitchtools.expr_has_duplicate_numbered_chromatic_pitch_class(skiptools.Skip((1, 4)))
