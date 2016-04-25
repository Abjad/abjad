# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RomanNumeral__initialize_by_symbolic_string_01():

    tonal_function = tonalanalysistools.RomanNumeral('bII')
    correct = tonalanalysistools.RomanNumeral(('flat', 2), 'major', 5, 0)
    assert tonal_function == correct

    tonal_function = tonalanalysistools.RomanNumeral('bII6')
    correct = tonalanalysistools.RomanNumeral(('flat', 2), 'major', 5, 1)
    assert tonal_function == correct

    tonal_function = tonalanalysistools.RomanNumeral('bII6/4')
    correct = tonalanalysistools.RomanNumeral(('flat', 2), 'major', 5, 2)
    assert tonal_function == correct


def test_tonalanalysistools_RomanNumeral__initialize_by_symbolic_string_02():

    tonal_function = tonalanalysistools.RomanNumeral('V7')
    correct = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0)
    assert tonal_function == correct

    tonal_function = tonalanalysistools.RomanNumeral('V6/5')
    correct = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 1)
    assert tonal_function == correct

    tonal_function = tonalanalysistools.RomanNumeral('V4/3')
    correct = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 2)
    assert tonal_function == correct

    tonal_function = tonalanalysistools.RomanNumeral('V4/2')
    correct = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 3)
    assert tonal_function == correct


def test_tonalanalysistools_RomanNumeral__initialize_by_symbolic_string_03():

    tonal_function = tonalanalysistools.RomanNumeral('V7/4-3')
    correct = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0, (4, 3))
    assert tonal_function == correct

    tonal_function = tonalanalysistools.RomanNumeral('V6/5/4-3')
    correct = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 1, (4, 3))
    assert tonal_function == correct


def test_tonalanalysistools_RomanNumeral__initialize_by_symbolic_string_04():

    tonal_function = tonalanalysistools.RomanNumeral('vi6/5')
    correct = tonalanalysistools.RomanNumeral(6, 'minor', 7, 1)
    assert tonal_function == correct
