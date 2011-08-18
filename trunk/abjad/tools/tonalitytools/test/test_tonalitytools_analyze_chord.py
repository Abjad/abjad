from abjad import *
from abjad.tools import tonalitytools


def test_tonalitytools_analyze_chord_01():
    '''The three inversions of a C major triad.'''

    chord_class = tonalitytools.analyze_chord(Chord([0, 4, 7], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'major', 'triad', 'root')

    chord_class = tonalitytools.analyze_chord(Chord([4, 7, 12], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'major', 'triad', 1)

    chord_class = tonalitytools.analyze_chord(Chord([7, 12, 16], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'major', 'triad', 2)


def test_tonalitytools_analyze_chord_02():
    '''The three inversions of an a minor triad.'''

    chord_class = tonalitytools.analyze_chord(Chord([9, 12, 16], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('a', 'minor', 'triad', 'root')

    chord_class = tonalitytools.analyze_chord(Chord([12, 16, 21], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('a', 'minor', 'triad', 1)

    chord_class = tonalitytools.analyze_chord(Chord([16, 21, 24], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('a', 'minor', 'triad', 2)


def test_tonalitytools_analyze_chord_03():
    '''The four inversions of a C dominant seventh chord.'''

    chord_class = tonalitytools.analyze_chord(Chord([0, 4, 7, 10], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'dominant', 7, 'root')

    chord_class = tonalitytools.analyze_chord(Chord([4, 7, 10, 12], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'dominant', 7, 1)

    chord_class = tonalitytools.analyze_chord(Chord([7, 10, 12, 16], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'dominant', 7, 2)

    chord_class = tonalitytools.analyze_chord(Chord([10, 12, 16, 19], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'dominant', 7, 3)


def test_tonalitytools_analyze_chord_04():
    '''The five inversions of a C dominant ninth chord.'''

    chord_class = tonalitytools.analyze_chord(Chord([0, 4, 7, 10, 14], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'dominant', 9, 'root')

    chord_class = tonalitytools.analyze_chord(Chord([4, 7, 10, 12, 14], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'dominant', 9, 1)

    chord_class = tonalitytools.analyze_chord(Chord([7, 10, 12, 14, 16], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'dominant', 9, 2)

    chord_class = tonalitytools.analyze_chord(Chord([10, 12, 14, 16, 19], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'dominant', 9, 3)

    chord_class = tonalitytools.analyze_chord(Chord([2, 10, 12, 16, 19], (1, 4)))
    assert chord_class == tonalitytools.ChordClass('c', 'dominant', 9, 4)


def test_tonalitytools_analyze_chord_05():
    '''Return none when chord does not analyze.'''

    chord_class = tonalitytools.analyze_chord(Chord(['c', 'cs', 'd'], (1, 4)))
    assert chord_class is None
