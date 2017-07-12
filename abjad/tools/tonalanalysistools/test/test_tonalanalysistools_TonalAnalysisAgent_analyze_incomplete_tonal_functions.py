# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_TonalAnalysisAgent_analyze_incomplete_tonal_functions_01():

    chord = abjad.Chord("<g' b'>4")
    key_signature = abjad.KeySignature('c', 'major')
    tonal_function = tonalanalysistools.RomanNumeral('V')
    selection = abjad.analyze(chord)
    result = selection.analyze_incomplete_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = abjad.Chord("<g' bf'>4")
    tonal_function = tonalanalysistools.RomanNumeral('v')
    selection = abjad.analyze(chord)
    result = selection.analyze_incomplete_tonal_functions(key_signature)
    assert result == [tonal_function]


def test_tonalanalysistools_TonalAnalysisAgent_analyze_incomplete_tonal_functions_02():

    key_signature = abjad.KeySignature('c', 'major')
    chord = abjad.Chord("<f g b>4")
    tonal_function = tonalanalysistools.RomanNumeral('V4/3')
    selection = abjad.analyze(chord)
    result = selection.analyze_incomplete_tonal_functions(key_signature)
    assert result == [tonal_function]

    chord = abjad.Chord("<fs g b>4")
    tonal_function = tonalanalysistools.RomanNumeral('VM4/3')
    selection = abjad.analyze(chord)
    result = selection.analyze_incomplete_tonal_functions(key_signature)
    assert result == [tonal_function]
