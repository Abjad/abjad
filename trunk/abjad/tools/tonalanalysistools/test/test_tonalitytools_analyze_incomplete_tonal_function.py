from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_analyze_incomplete_tonal_function_01():

    key_signature = contexttools.KeySignatureMark('c', 'major')
    tf = tonalanalysistools.analyze_incomplete_tonal_function(Chord("<g' b'>4"), key_signature)
    assert tf == tonalanalysistools.TonalFunction('V')

    tf = tonalanalysistools.analyze_incomplete_tonal_function(Chord("<g' bf'>4"), key_signature)
    assert tf == tonalanalysistools.TonalFunction('v')


def test_tonalanalysistools_analyze_incomplete_tonal_function_02():

    key_signature = contexttools.KeySignatureMark('c', 'major')
    tf = tonalanalysistools.analyze_incomplete_tonal_function(Chord("<f g b>4"), key_signature)
    assert tf == tonalanalysistools.TonalFunction('V4/3')

    tf = tonalanalysistools.analyze_incomplete_tonal_function(Chord("<fs g b>4"), key_signature)
    assert tf == tonalanalysistools.TonalFunction('VM4/3')
