from abjad import *
from abjad.tools import tonalitytools


def test_tonalitytools_analyze_incomplete_tonal_function_01():

    key_signature = contexttools.KeySignatureMark('c', 'major')
    tf = tonalitytools.analyze_incomplete_tonal_function(Chord("<g' b'>4"), key_signature)
    assert tf == tonalitytools.TonalFunction('V')

    tf = tonalitytools.analyze_incomplete_tonal_function(Chord("<g' bf'>4"), key_signature)
    assert tf == tonalitytools.TonalFunction('v')


def test_tonalitytools_analyze_incomplete_tonal_function_02():

    key_signature = contexttools.KeySignatureMark('c', 'major')
    tf = tonalitytools.analyze_incomplete_tonal_function(Chord("<f g b>4"), key_signature)
    assert tf == tonalitytools.TonalFunction('V4/3')

    tf = tonalitytools.analyze_incomplete_tonal_function(Chord("<fs g b>4"), key_signature)
    assert tf == tonalitytools.TonalFunction('VM4/3')
