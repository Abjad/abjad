# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RomanNumeral___init___01():
    r'''Initializes roman numeral from empty input.
    '''

    roman_numeral = tonalanalysistools.RomanNumeral()

    assert repr(roman_numeral) == 'IMajorTriadInRootPosition'
