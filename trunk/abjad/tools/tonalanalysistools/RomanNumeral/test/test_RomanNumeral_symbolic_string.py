# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_RomanNumeral_symbolic_string_01():

    t = tonalanalysistools.RomanNumeral(5, 'dominant', 7, 0, (4, 3))
    assert t.symbolic_string == 'V7/4-3'

    t = tonalanalysistools.RomanNumeral(2, 'minor', 7, 1)
    assert t.symbolic_string == 'ii6/5'

    t = tonalanalysistools.RomanNumeral(1, 'major', 5, 1)
    assert t.symbolic_string == 'I6'
