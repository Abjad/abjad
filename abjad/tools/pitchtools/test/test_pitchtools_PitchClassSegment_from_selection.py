# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment_from_selection_01():
    r'''Works with notes.
    '''

    note = Note(13, (1, 4))
    assert pitchtools.PitchClassSegment.from_selection(
        note,
        item_class=pitchtools.NumberedPitchClass,
        ) == (pitchtools.NumberedPitchClass(1), )


def test_pitchtools_PitchClassSegment_from_selection_02():
    r'''Works with multiple-note chords.
    '''

    chord = Chord([13, 14, 15], (1, 4))
    assert pitchtools.PitchClassSegment.from_selection(
        chord,
        item_class=pitchtools.NumberedPitchClass,
        ) == (
        pitchtools.NumberedPitchClass(1),
        pitchtools.NumberedPitchClass(2),
        pitchtools.NumberedPitchClass(3))


def test_pitchtools_PitchClassSegment_from_selection_03():
    r'''Works with one-note chords.
    '''

    chord = Chord([13], (1, 4))
    assert pitchtools.PitchClassSegment.from_selection(
        chord,
        item_class=pitchtools.NumberedPitchClass,
        ) == (pitchtools.NumberedPitchClass(1), )


def test_pitchtools_PitchClassSegment_from_selection_04():
    r'''Works with empty chords.
    '''

    chord = Chord([], (1, 4))
    assert pitchtools.PitchClassSegment.from_selection(
        chord,
        item_class=pitchtools.NumberedPitchClass,
        ) == ()
