# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_TonalAnalysisAgent_analyze_chords_01():
    r'''The three inversions of a C major triad.
    '''

    chord = Chord([0, 4, 7], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'major', 'triad', 'root')
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([4, 7, 12], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'major', 'triad', 1)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([7, 12, 16], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'major', 'triad', 2)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_chords_02():
    r'''The three inversions of an a minor triad.
    '''

    chord = Chord([9, 12, 16], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('a', 'minor', 'triad', 'root')
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([12, 16, 21], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('a', 'minor', 'triad', 1)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([16, 21, 24], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('a', 'minor', 'triad', 2)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_chords_03():
    r'''The four inversions of a C dominant seventh chord.
    '''

    chord = Chord([0, 4, 7, 10], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'dominant', 7, 'root')
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([4, 7, 10, 12], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'dominant', 7, 1)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([7, 10, 12, 16], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'dominant', 7, 2)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([10, 12, 16, 19], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'dominant', 7, 3)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_chords_04():
    r'''The five inversions of a C dominant ninth chord.
    '''

    chord = Chord([0, 4, 7, 10, 14], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'dominant', 9, 'root')
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([4, 7, 10, 12, 14], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'dominant', 9, 1)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([7, 10, 12, 14, 16], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'dominant', 9, 2)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([10, 12, 14, 16, 19], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'dominant', 9, 3)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]

    chord = Chord([2, 10, 12, 16, 19], (1, 4))
    chord_class = tonalanalysistools.RootedChordClass('c', 'dominant', 9, 4)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [chord_class]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_chords_05():
    r'''Returns none when chord does not analyze.
    '''

    chord = Chord('<c cs d>4')
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_chords() == [None]
