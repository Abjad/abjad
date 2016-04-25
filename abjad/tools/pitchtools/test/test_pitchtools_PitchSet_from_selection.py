# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSet_from_selection_01():
    r'''Works with notes.
    '''

    note = Note(13, (1, 4))
    pitch_set = pitchtools.PitchSet.from_selection(note)
    assert len(pitch_set) == 1


def test_pitchtools_PitchSet_from_selection_02():
    r'''Works with chords.
    '''

    chord = Chord([13, 14, 15], (1, 4))
    pitch_set = pitchtools.PitchSet.from_selection(chord)
    assert len(pitch_set) == 3


def test_pitchtools_PitchSet_from_selection_03():
    r'''Works with chords with duplicate pitches.
    '''

    chord = Chord([13, 13, 13, 14], (1, 4))
    pitch_set = pitchtools.PitchSet.from_selection(chord)
    assert len(pitch_set) == 2


def test_pitchtools_PitchSet_from_selection_04():
    r'''Works with empty chords.
    '''

    chord = Chord([], (1, 4))
    pitch_set = pitchtools.PitchSet.from_selection(chord)
    assert len(pitch_set) == 0


def test_pitchtools_PitchSet_from_selection_05():
    r'''Works with chords.
    '''

    assert len(pitchtools.PitchSet.from_selection(
        Chord([12, 14, 18, 19], (1, 4)))) == 4
