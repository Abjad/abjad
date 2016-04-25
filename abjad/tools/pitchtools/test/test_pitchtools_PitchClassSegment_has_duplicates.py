# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSegment_has_duplicates_01():
    r'''Works with chords.
    '''

    chord = Chord([1, 13, 14], (1, 4))
    assert pitchtools.PitchClassSegment.from_selection(
        chord,
        item_class=pitchtools.NumberedPitchClass,
        ).has_duplicates

    chord = Chord([1, 14, 15], (1, 4))
    assert not pitchtools.PitchClassSegment.from_selection(
        chord,
        item_class=pitchtools.NumberedPitchClass,
        ).has_duplicates


def test_pitchtools_PitchClassSegment_has_duplicates_02():
    r'''Works with notes, rests and skips.
    '''

    assert not pitchtools.PitchClassSegment.from_selection(
        Note(13, (1, 4)),
        item_class=pitchtools.NumberedPitchClass,
        ).has_duplicates
    assert not pitchtools.PitchClassSegment.from_selection(
        Rest((1, 4)),
        item_class=pitchtools.NumberedPitchClass,
        ).has_duplicates
    assert not pitchtools.PitchClassSegment.from_selection(
        scoretools.Skip((1, 4)),
        item_class=pitchtools.NumberedPitchClass,
        ).has_duplicates
