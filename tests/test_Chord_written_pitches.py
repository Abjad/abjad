import abjad
import pytest


def test_Chord_written_pitches_01():
    """
    Returns immutable tuple of pitches in chord.
    """

    chord = abjad.Chord("<d' e' f'>4")
    pitches = chord.written_pitches

    assert isinstance(pitches, abjad.PitchSegment)
    assert len(pitches) == 3
    with pytest.raises(Exception):
        pitches.pop()
    with pytest.raises(Exception):
        pitches.remove(pitches[0])


def test_Chord_written_pitches_02():
    """
    Equivalent written pitches compare equal.
    """

    chord_1 = abjad.Chord("<d' e' f'>4")
    chord_2 = abjad.Chord("<d' e' f'>4")

    assert chord_1.written_pitches == chord_2.written_pitches


def test_Chord_written_pitches_03():
    """
    Set written pitches with pitch numbers.
    """

    chord = abjad.Chord([], (1, 4))
    chord.written_pitches = [4, 3, 2]
    assert format(chord) == "<d' ef' e'>4"

    chord.written_pitches = (4, 3, 2)
    assert format(chord) == "<d' ef' e'>4"


def test_Chord_written_pitches_04():
    """
    Set written pitches with pitches.
    """

    chord = abjad.Chord([], (1, 4))
    chord.written_pitches = [
        abjad.NamedPitch(4),
        abjad.NamedPitch(3),
        abjad.NamedPitch(2),
    ]

    assert format(chord) == "<d' ef' e'>4"


def test_Chord_written_pitches_05():
    """
    Set written pitches with both pitches and pitch numbers.
    """

    chord = abjad.Chord([], (1, 4))
    chord.written_pitches = [4, abjad.NamedPitch(3), abjad.NamedPitch(2)]

    assert format(chord) == "<d' ef' e'>4"
