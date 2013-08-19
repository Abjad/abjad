# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_list_numbered_chromatic_pitch_classes_in_expr_01():
    r'''Works with notes.
    '''

    note = Note(13, (1, 4))
    assert pitchtools.list_numbered_chromatic_pitch_classes_in_expr(note) == (pitchtools.NumberedPitchClass(1), )


def test_pitchtools_list_numbered_chromatic_pitch_classes_in_expr_02():
    r'''Works with multiple-note chords.
    '''

    chord = Chord([13, 14, 15], (1, 4))
    assert pitchtools.list_numbered_chromatic_pitch_classes_in_expr(chord) == (
        pitchtools.NumberedPitchClass(1),
        pitchtools.NumberedPitchClass(2),
        pitchtools.NumberedPitchClass(3))


def test_pitchtools_list_numbered_chromatic_pitch_classes_in_expr_03():
    r'''Works with one-note chords.
    '''

    chord = Chord([13], (1, 4))
    assert pitchtools.list_numbered_chromatic_pitch_classes_in_expr(chord) == (pitchtools.NumberedPitchClass(1), )


def test_pitchtools_list_numbered_chromatic_pitch_classes_in_expr_04():
    r'''Works with empty chords.
    '''

    chord = Chord([], (1, 4))
    assert pitchtools.list_numbered_chromatic_pitch_classes_in_expr(chord) == ()
