# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_RomanNumeral___eq___01():

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0)
    u = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0, (4, 3))
    v = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0, (4, 3))

    assert      roman_numeral == roman_numeral
    assert not roman_numeral == u
    assert not roman_numeral == v

    assert not u == roman_numeral
    assert      u == u
    assert      u == v

    assert not v == roman_numeral
    assert      v == u
    assert      v == v
