from abjad import *


def test_chordtools_get_arithmetic_mean_of_chord_01():
    '''Chord mean equals the arithmetic mean of all pitch numbers in chord.
    '''

    chord = Chord([0, 2, 9, 10], (1, 4))
    assert chordtools.get_arithmetic_mean_of_chord(chord) == 5.25


def test_chordtools_get_arithmetic_mean_of_chord_02():
    '''Chord mean of one-note chord equals the pitch of the chord.
    '''

    chord = Chord([8], (1, 4))
    assert chordtools.get_arithmetic_mean_of_chord(chord) == 8


def test_chordtools_get_arithmetic_mean_of_chord_03():
    '''Chord mean of empty chord returns none.
    '''

    chord = Chord([], (1, 4))
    assert chordtools.get_arithmetic_mean_of_chord(chord) is None
