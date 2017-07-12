# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_TonalAnalysisAgent_analyze_incomplete_chords_01():

    chord = abjad.Chord('<g b>4')
    chord_class = tonalanalysistools.RootedChordClass('g', 'major', 'triad', 'root')
    selection = abjad.analyze(chord)
    assert selection.analyze_incomplete_chords() == [chord_class]

    chord = abjad.Chord('<g bf>4')
    chord_class = tonalanalysistools.RootedChordClass('g', 'minor', 'triad', 'root')
    selection = abjad.analyze(chord)
    assert selection.analyze_incomplete_chords() == [chord_class]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_incomplete_chords_02():

    chord = abjad.Chord('<f g b>4')
    chord_class = tonalanalysistools.RootedChordClass('g', 'dominant', 'seventh', 2)
    selection = abjad.analyze(chord)
    assert selection.analyze_incomplete_chords() == [chord_class]

    chord = abjad.Chord('<fs g b>4')
    chord_class = tonalanalysistools.RootedChordClass('g', 'major', 'seventh', 2)
    selection = abjad.analyze(chord)
    assert selection.analyze_incomplete_chords() == [chord_class]
