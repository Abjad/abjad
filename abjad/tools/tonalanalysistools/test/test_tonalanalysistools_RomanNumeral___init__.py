# -*- encoding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_RomanNumeral___init___01():
    r'''Initializes roman numeral from empty input.
    '''

    roman_numeral = tonalanalysistools.RomanNumeral()

    assert format(roman_numeral) == 'IMajorTriadInRootPosition'
