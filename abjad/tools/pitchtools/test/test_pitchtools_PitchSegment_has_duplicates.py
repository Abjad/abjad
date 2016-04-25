# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchSegment_has_duplicates_01():
    r'''Works with chords.
    '''

    assert pitchtools.PitchSegment.from_selection(
        Chord([13, 13, 14], (1, 4))).has_duplicates
    assert not pitchtools.PitchSegment.from_selection(
        Chord([13, 14], (1, 4))).has_duplicates
    assert not pitchtools.PitchSegment.from_selection(
        Chord([], (1, 4))).has_duplicates


def test_pitchtools_PitchSegment_has_duplicates_02():
    r'''Works with notes, rests and skips.
    '''

    assert not pitchtools.PitchSegment.from_selection(
        Note(13, (1, 4))).has_duplicates
    assert not pitchtools.PitchSegment.from_selection(
        Rest((1, 4))).has_duplicates
    assert not pitchtools.PitchSegment.from_selection(
        scoretools.Skip((1, 4))).has_duplicates


def test_pitchtools_PitchSegment_has_duplicates_03():
    r'''Works with containers.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")
    assert pitchtools.PitchSegment.from_selection(staff).has_duplicates

    staff = Staff("c'8 d'8 e'8 f'8")
    assert not pitchtools.PitchSegment.from_selection(staff).has_duplicates
