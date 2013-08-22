# -*- encoding: utf-8 -*-
from abjad import *


def test_TonalAnalysisAgent_analyze_incomplete_chords_01():

    chord = Chord('<g b>4')
    chord_class = tonalanalysistools.ChordClass('g', 'major', 'triad', 'root')
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_incomplete_chords() == [chord_class]

    chord = Chord('<g bf>4')
    chord_class = tonalanalysistools.ChordClass('g', 'minor', 'triad', 'root')
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_incomplete_chords() == [chord_class]


def test_TonalAnalysisAgent_analyze_incomplete_chords_02():

    chord = Chord('<f g b>4')
    chord_class = tonalanalysistools.ChordClass('g', 'dominant', 'seventh', 2)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_incomplete_chords() == [chord_class]

    chord = Chord('<fs g b>4')
    chord_class = tonalanalysistools.ChordClass('g', 'major', 'seventh', 2)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_incomplete_chords() == [chord_class]
