# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange_list_octave_transpositions_01():
    r'''Works on chords.
    '''

    chord = Chord([0, 2, 4], (1, 4))
    pitch_range = pitchtools.PitchRange.from_pitches(0, 48)
    transpositions = pitch_range.list_octave_transpositions(chord)

    r"""
    [Chord(c' d' e', 4),
    Chord(c'' d'' e'', 4),
    Chord(c''' d''' e''', 4),
    Chord(c'''' d'''' e'''', 4)]
    """

    assert len(transpositions) == 4
    assert format(transpositions[0]) == "<c' d' e'>4"
    assert format(transpositions[1]) ==  "<c'' d'' e''>4"
    assert format(transpositions[2]) == "<c''' d''' e'''>4"
    assert format(transpositions[3]) == "<c'''' d'''' e''''>4"


def test_pitchtools_PitchRange_list_octave_transpositions_02():
    r'''Works on pitch numbers.
    '''

    pitch_numbers = [0, 2, 4]
    pitch_range = pitchtools.PitchRange.from_pitches(0, 48)
    transpositions = pitch_range.list_octave_transpositions(pitch_numbers)

    assert transpositions == [[0, 2, 4], [12, 14, 16], [24, 26, 28], [36, 38, 40]]
