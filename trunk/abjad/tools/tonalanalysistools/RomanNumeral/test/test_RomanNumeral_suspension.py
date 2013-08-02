# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_RomanNumeral_suspension_01():

    t = tonalanalysistools.RomanNumeral(5, 'major', 5, 0, (4, 3))

    assert t.suspension == tonalanalysistools.SuspensionIndicator(4, 3)
    assert t.suspension.start == tonalanalysistools.ScaleDegree(4)
    assert t.suspension.stop == tonalanalysistools.ScaleDegree(3)
