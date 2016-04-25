# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_RomanNumeral___eq___01():

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0)
    u = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0, (4, 3))
    voice = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0, (4, 3))

    assert      roman_numeral == roman_numeral
    assert not roman_numeral == u
    assert not roman_numeral == voice

    assert not u == roman_numeral
    assert      u == u
    assert      u == voice

    assert not voice == roman_numeral
    assert      voice == u
    assert      voice == voice
