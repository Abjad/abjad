from abjad import *
from abjad.tools import tonalitytools


def test_tonalitytools_analyze_incomplete_chord_01():

    cc = tonalitytools.analyze_incomplete_chord(Chord(['g', 'b'], (1, 4)))
    assert cc == tonalitytools.ChordClass('g', 'major', 'triad', 'root')

    cc = tonalitytools.analyze_incomplete_chord(Chord(['g', 'bf'], (1, 4)))
    assert cc == tonalitytools.ChordClass('g', 'minor', 'triad', 'root')


def test_tonalitytools_analyze_incomplete_chord_02():

    cc = tonalitytools.analyze_incomplete_chord(Chord(['f', 'g', 'b'], (1, 4)))
    assert cc == tonalitytools.ChordClass('g', 'dominant', 'seventh', 2)

    cc = tonalitytools.analyze_incomplete_chord(Chord(['fs', 'g', 'b'], (1, 4)))
    assert cc == tonalitytools.ChordClass('g', 'major', 'seventh', 2)
