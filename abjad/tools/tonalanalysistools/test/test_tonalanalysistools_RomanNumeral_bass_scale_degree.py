# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RomanNumeral_bass_scale_degree_01():

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'major', 5, 0)
    assert roman_numeral.bass_scale_degree == tonalanalysistools.ScaleDegree(5)

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'major', 5, 1)
    assert roman_numeral.bass_scale_degree == tonalanalysistools.ScaleDegree(7)

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'major', 5, 2)
    assert roman_numeral.bass_scale_degree == tonalanalysistools.ScaleDegree(2)


def test_tonalanalysistools_RomanNumeral_bass_scale_degree_02():

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'major', 7, 0)
    assert roman_numeral.bass_scale_degree == tonalanalysistools.ScaleDegree(5)

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'major', 7, 1)
    assert roman_numeral.bass_scale_degree == tonalanalysistools.ScaleDegree(7)

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'major', 7, 2)
    assert roman_numeral.bass_scale_degree == tonalanalysistools.ScaleDegree(2)

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'major', 7, 3)
    assert roman_numeral.bass_scale_degree == tonalanalysistools.ScaleDegree(4)
