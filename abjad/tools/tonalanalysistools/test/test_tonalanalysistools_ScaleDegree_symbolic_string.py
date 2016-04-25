# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree_symbolic_string_01():

    assert tonalanalysistools.ScaleDegree(1).symbolic_string == 'I'
    assert tonalanalysistools.ScaleDegree('flat', 2).symbolic_string == 'bII'
    assert tonalanalysistools.ScaleDegree(3).symbolic_string == 'III'
    assert tonalanalysistools.ScaleDegree('sharp', 4).symbolic_string == '#IV'
    assert tonalanalysistools.ScaleDegree(5).symbolic_string == 'V'
    assert tonalanalysistools.ScaleDegree('flat', 6).symbolic_string == 'bVI'
    assert tonalanalysistools.ScaleDegree('flat', 7).symbolic_string == 'bVII'
