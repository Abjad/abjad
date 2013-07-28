from abjad import *


def test_TonalAnalysisSelection_analyze_tonal_functions_01():

    key_signature = contexttools.KeySignatureMark('c', 'major')
    chord = Chord('<c e g>4')
    tonal_function = tonalanalysistools.TonalFunction(1, 'major', 5, 0)
    selection = tonalanalysistools.select(chord)
    assert selection.analyze_tonal_functions(key_signature) == [tonal_function]

    chord = Chord(['e', 'g', "c'"], (1, 4))
    tonal_function = tonalanalysistools.analyze_tonal_function(chord, key_signature)
    correct_tonal_function = tonalanalysistools.TonalFunction(1, 'major', 5, 1)
    assert tonal_function == correct_tonal_function

    chord = Chord(['g', "c'", "e'"], (1, 4))
    tonal_function = tonalanalysistools.analyze_tonal_function(chord, key_signature)
    correct_tonal_function = tonalanalysistools.TonalFunction(1, 'major', 5, 2)
    assert tonal_function == correct_tonal_function


def test_TonalAnalysisSelection_analyze_tonal_functions_02():

    key_signature = contexttools.KeySignatureMark('c', 'major')
    chord = Chord(['c', 'ef', 'g'], (1, 4))
    tonal_function = tonalanalysistools.analyze_tonal_function(chord, key_signature)
    correct_tonal_function = tonalanalysistools.TonalFunction(1, 'minor', 5, 0)
    assert tonal_function == correct_tonal_function

    chord = Chord(['ef', 'g', "c'"], (1, 4))
    tonal_function = tonalanalysistools.analyze_tonal_function(chord, key_signature)
    correct_tonal_function = tonalanalysistools.TonalFunction(1, 'minor', 5, 1)
    assert tonal_function == correct_tonal_function

    chord = Chord(['g', "c'", "ef'"], (1, 4))
    tonal_function = tonalanalysistools.analyze_tonal_function(chord, key_signature)
    correct_tonal_function = tonalanalysistools.TonalFunction(1, 'minor', 5, 2)
    assert tonal_function == correct_tonal_function


def test_TonalAnalysisSelection_analyze_tonal_functions_03():

    key_signature = contexttools.KeySignatureMark('c', 'major')
    chord = Chord(['c', 'e', 'g', 'bf'], (1, 4))
    tonal_function = tonalanalysistools.analyze_tonal_function(chord, key_signature)
    correct_tonal_function = tonalanalysistools.TonalFunction(1, 'dominant', 7, 0)
    assert tonal_function == correct_tonal_function

    chord = Chord(['e', 'g', 'bf', "c'"], (1, 4))
    tonal_function = tonalanalysistools.analyze_tonal_function(chord, key_signature)
    correct_tonal_function = tonalanalysistools.TonalFunction(1, 'dominant', 7, 1)
    assert tonal_function == correct_tonal_function

    chord = Chord(['g', 'bf', "c'", "e'"], (1, 4))
    tonal_function = tonalanalysistools.analyze_tonal_function(chord, key_signature)
    correct_tonal_function = tonalanalysistools.TonalFunction(1, 'dominant', 7, 2)
    assert tonal_function == correct_tonal_function

    chord = Chord(['bf', "c'", "e'", "g'"], (1, 4))
    tonal_function = tonalanalysistools.analyze_tonal_function(chord, key_signature)
    correct_tonal_function = tonalanalysistools.TonalFunction(1, 'dominant', 7, 3)
    assert tonal_function == correct_tonal_function


def test_TonalAnalysisSelection_analyze_tonal_functions_04():

    key_signature = contexttools.KeySignatureMark('c', 'major')
    chord = Chord(['c', 'cs', 'd'], (1, 4))
    tonal_function = tonalanalysistools.analyze_tonal_function(chord, key_signature)
    assert tonal_function is None
