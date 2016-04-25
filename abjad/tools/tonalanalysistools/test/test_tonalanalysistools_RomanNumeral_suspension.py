# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RomanNumeral_suspension_01():

    roman_numeral = tonalanalysistools.RomanNumeral(5, 'major', 5, 0, (4, 3))

    assert roman_numeral.suspension == tonalanalysistools.ChordSuspension(4, 3)
    assert roman_numeral.suspension.start == tonalanalysistools.ScaleDegree(4)
    assert roman_numeral.suspension.stop == tonalanalysistools.ScaleDegree(3)
