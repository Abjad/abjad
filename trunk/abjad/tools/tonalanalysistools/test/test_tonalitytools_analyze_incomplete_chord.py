from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_analyze_incomplete_chord_01():

    cc = tonalanalysistools.analyze_incomplete_chord(Chord(['g', 'b'], (1, 4)))
    assert cc == tonalanalysistools.ChordClass('g', 'major', 'triad', 'root')

    cc = tonalanalysistools.analyze_incomplete_chord(Chord(['g', 'bf'], (1, 4)))
    assert cc == tonalanalysistools.ChordClass('g', 'minor', 'triad', 'root')


def test_tonalanalysistools_analyze_incomplete_chord_02():

    cc = tonalanalysistools.analyze_incomplete_chord(Chord(['f', 'g', 'b'], (1, 4)))
    assert cc == tonalanalysistools.ChordClass('g', 'dominant', 'seventh', 2)

    cc = tonalanalysistools.analyze_incomplete_chord(Chord(['fs', 'g', 'b'], (1, 4)))
    assert cc == tonalanalysistools.ChordClass('g', 'major', 'seventh', 2)
