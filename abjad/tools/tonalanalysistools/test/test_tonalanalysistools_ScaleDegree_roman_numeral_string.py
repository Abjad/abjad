# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree_roman_numeral_string_01():

    assert tonalanalysistools.ScaleDegree(1).roman_numeral_string == 'I'
    assert tonalanalysistools.ScaleDegree(2).roman_numeral_string == 'II'
    assert tonalanalysistools.ScaleDegree(3).roman_numeral_string == 'III'
    assert tonalanalysistools.ScaleDegree(4).roman_numeral_string == 'IV'
    assert tonalanalysistools.ScaleDegree(5).roman_numeral_string == 'V'
    assert tonalanalysistools.ScaleDegree(6).roman_numeral_string == 'VI'
    assert tonalanalysistools.ScaleDegree(7).roman_numeral_string == 'VII'
