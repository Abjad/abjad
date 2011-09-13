from abjad import *


def test_pitchtools_expr_has_duplicate_named_chromatic_pitch_01():
    '''Works with chords.'''

    assert pitchtools.expr_has_duplicate_named_chromatic_pitch(Chord([13, 13, 14], (1, 4)))
    assert not pitchtools.expr_has_duplicate_named_chromatic_pitch(Chord([13, 14], (1, 4)))
    assert not pitchtools.expr_has_duplicate_named_chromatic_pitch(Chord([], (1, 4)))


def test_pitchtools_expr_has_duplicate_named_chromatic_pitch_02():
    '''Works with notes, rests and skips.'''

    assert not pitchtools.expr_has_duplicate_named_chromatic_pitch(Note(13, (1, 4)))
    assert not pitchtools.expr_has_duplicate_named_chromatic_pitch(Rest((1, 4)))
    assert not pitchtools.expr_has_duplicate_named_chromatic_pitch(skiptools.Skip((1, 4)))


def test_pitchtools_expr_has_duplicate_named_chromatic_pitch_03():
    '''Works with containers.'''

    staff = Staff(notetools.make_repeated_notes(4))
    assert pitchtools.expr_has_duplicate_named_chromatic_pitch(staff)

    staff = Staff("c'8 d'8 e'8 f'8")
    assert not pitchtools.expr_has_duplicate_named_chromatic_pitch(staff)
