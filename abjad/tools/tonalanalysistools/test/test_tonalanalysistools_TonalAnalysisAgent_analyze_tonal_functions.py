# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_TonalAnalysisAgent_analyze_tonal_functions_01():

    key_signature = abjad.KeySignature('c', 'major')
    chord = abjad.Chord('<c e g>4')
    tonal_function = tonalanalysistools.RomanNumeral(1, 'major', 5, 0)
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = abjad.Chord(['e', 'g', "c'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'major', 5, 1)
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = abjad.Chord(['g', "c'", "e'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'major', 5, 2)
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_tonal_functions_02():

    key_signature = abjad.KeySignature('c', 'major')
    chord = abjad.Chord(['c', 'ef', 'g'], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'minor', 5, 0)
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = abjad.Chord(['ef', 'g', "c'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'minor', 5, 1)
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = abjad.Chord(['g', "c'", "ef'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'minor', 5, 2)
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_tonal_functions_03():

    key_signature = abjad.KeySignature('c', 'major')
    chord = abjad.Chord(['c', 'e', 'g', 'bf'], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'dominant', 7, 0)
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = abjad.Chord(['e', 'g', 'bf', "c'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'dominant', 7, 1)
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = abjad.Chord(['g', 'bf', "c'", "e'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'dominant', 7, 2)
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = abjad.Chord(['bf', "c'", "e'", "g'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'dominant', 7, 3)
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_tonal_functions_04():

    key_signature = abjad.KeySignature('c', 'major')
    chord = abjad.Chord(['c', 'cs', 'd'], (1, 4))
    selection = abjad.analyze(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [None]
