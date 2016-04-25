# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RomanNumeral_symbolic_string_01():

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0, (4, 3))
    assert roman_numeral.symbolic_string == 'V7/4-3'

    roman_numeral = tonalanalysistools.RomanNumeral(2, 'minor', 7, 1)
    assert roman_numeral.symbolic_string == 'ii6/5'

    roman_numeral = tonalanalysistools.RomanNumeral(1, 'major', 5, 1)
    assert roman_numeral.symbolic_string == 'I6'
