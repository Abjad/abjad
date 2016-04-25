# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_TonalAnalysisAgent_analyze_incomplete_tonal_functions_01():

    chord = Chord("<g' b'>4")
    key_signature = KeySignature('c', 'major')
    tonal_function = tonalanalysistools.RomanNumeral('V')
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_incomplete_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = Chord("<g' bf'>4")
    tonal_function = tonalanalysistools.RomanNumeral('v')
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_incomplete_tonal_functions(key_signature)
    assert result == [tonal_function]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_incomplete_tonal_functions_02():

    key_signature = KeySignature('c', 'major')
    chord = Chord("<f g b>4")
    tonal_function = tonalanalysistools.RomanNumeral('V4/3')
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_incomplete_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = Chord("<fs g b>4")
    tonal_function = tonalanalysistools.RomanNumeral('VM4/3')
    selection = tonalanalysistools.select(chord)
    result = selection.analyze_incomplete_tonal_functions(key_signature)
    assert result == [tonal_function]
