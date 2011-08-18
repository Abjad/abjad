from abjad import *
from abjad.tools import tonalitytools


def test_ScaleDegree_roman_numeral_string_01():

    assert tonalitytools.ScaleDegree(1).roman_numeral_string == 'I'
    assert tonalitytools.ScaleDegree(2).roman_numeral_string == 'II'
    assert tonalitytools.ScaleDegree(3).roman_numeral_string == 'III'
    assert tonalitytools.ScaleDegree(4).roman_numeral_string == 'IV'
    assert tonalitytools.ScaleDegree(5).roman_numeral_string == 'V'
    assert tonalitytools.ScaleDegree(6).roman_numeral_string == 'VI'
    assert tonalitytools.ScaleDegree(7).roman_numeral_string == 'VII'
