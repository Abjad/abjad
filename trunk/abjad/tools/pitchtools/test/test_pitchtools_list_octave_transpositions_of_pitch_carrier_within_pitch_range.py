from abjad import *


def test_pitchtools_list_octave_transpositions_of_pitch_carrier_within_pitch_range_01():
    '''Works on chords.
    '''

    chord = Chord([0, 2, 4], (1, 4))
    pitch_range = pitchtools.PitchRange(0, 48)
    transpositions = pitchtools.list_octave_transpositions_of_pitch_carrier_within_pitch_range(
        chord, pitch_range)

    r"""
    [Chord(c' d' e', 4),
    Chord(c'' d'' e'', 4),
    Chord(c''' d''' e''', 4),
    Chord(c'''' d'''' e'''', 4)]
    """

    assert len(transpositions) == 4
    assert transpositions[0].format == "<c' d' e'>4"
    assert transpositions[1].format ==  "<c'' d'' e''>4"
    assert transpositions[2].format == "<c''' d''' e'''>4"
    assert transpositions[3].format == "<c'''' d'''' e''''>4"


def test_pitchtools_list_octave_transpositions_of_pitch_carrier_within_pitch_range_02():
    '''Works on pitch numbers.
    '''

    pitch_numbers = [0, 2, 4]
    pitch_range = pitchtools.PitchRange(0, 48)
    transpositions = pitchtools.list_octave_transpositions_of_pitch_carrier_within_pitch_range(
        pitch_numbers, pitch_range)

    assert transpositions == [[0, 2, 4], [12, 14, 16], [24, 26, 28], [36, 38, 40]]
