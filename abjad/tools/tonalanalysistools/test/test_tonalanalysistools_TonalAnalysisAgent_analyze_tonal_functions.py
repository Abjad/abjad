# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_TonalAnalysisAgent_analyze_tonal_functions_01():

    key_signature = KeySignature('c', 'major')
    chord = Chord('<c e g>4')
    tonal_function = tonalanalysistools.RomanNumeral(1, 'major', 5, 0)
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = Chord(['e', 'g', "c'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'major', 5, 1)
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = Chord(['g', "c'", "e'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'major', 5, 2)
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_tonal_functions_02():

    key_signature = KeySignature('c', 'major')
    chord = Chord(['c', 'ef', 'g'], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'minor', 5, 0)
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = Chord(['ef', 'g', "c'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'minor', 5, 1)
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = Chord(['g', "c'", "ef'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'minor', 5, 2)
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_tonal_functions_03():

    key_signature = KeySignature('c', 'major')
    chord = Chord(['c', 'e', 'g', 'bf'], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'dominant', 7, 0)
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = Chord(['e', 'g', 'bf', "c'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'dominant', 7, 1)
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = Chord(['g', 'bf', "c'", "e'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'dominant', 7, 2)
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = Chord(['bf', "c'", "e'", "g'"], (1, 4))
    tonal_function = tonalanalysistools.RomanNumeral(1, 'dominant', 7, 3)
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [tonal_function]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_tonal_functions_04():

    key_signature = KeySignature('c', 'major')
    chord = Chord(['c', 'cs', 'd'], (1, 4))
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_tonal_functions(key_signature)
    assert result == [None]
