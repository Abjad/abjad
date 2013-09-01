# -*- encoding: utf-8 -*-
from abjad import *


def test_PitchSet___init___01():
    r'''Works with numbers.
    '''

    assert len(pitchtools.PitchSet([12, 14, 18, 19])) == 4


def test_PitchSet___init___02():
    r'''Works with pitches.
    '''

    assert len(pitchtools.PitchSet([pitchtools.NamedPitch(x) 
        for x in [12, 14, 18, 19]])) == 4


def test_PitchSet___init___03():
    r'''Works with notes.
    '''

    note = Note(13, (1, 4))
    pitch_set = pitchtools.PitchSet(
        pitchtools.list_named_chromatic_pitches_in_expr(note))
    assert len(pitch_set) == 1


def test_PitchSet___init___04():
    r'''Works with chords.
    '''

    chord = Chord([13, 14, 15], (1, 4))
    pitch_set = pitchtools.PitchSet(
        pitchtools.list_named_chromatic_pitches_in_expr(chord))
    assert len(pitch_set) == 3


def test_PitchSet___init___05():
    r'''Works with chords with duplicate pitches.
    '''

    chord = Chord([13, 13, 13, 14], (1, 4))
    pitch_set = pitchtools.PitchSet(
        pitchtools.list_named_chromatic_pitches_in_expr(chord))
    assert len(pitch_set) == 2


def test_PitchSet___init___06():
    r'''Works with empty chords.
    '''

    chord = Chord([], (1, 4))
    pitch_set = pitchtools.PitchSet(
        pitchtools.list_named_chromatic_pitches_in_expr(chord))
    assert len(pitch_set) == 0


def test_PitchSet___init___07():
    r'''Works with chords.
    '''

    assert len(pitchtools.PitchSet(Chord([12, 14, 18, 19], (1, 4)))) == 4
