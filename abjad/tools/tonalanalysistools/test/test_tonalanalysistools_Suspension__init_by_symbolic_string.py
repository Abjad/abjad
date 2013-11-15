# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Suspension__init_by_symbolic_string_01():

    suspension_indicator = tonalanalysistools.Suspension('4-3')
    assert suspension_indicator.start == tonalanalysistools.ScaleDegree(4)
    assert suspension_indicator.stop == tonalanalysistools.ScaleDegree(3)

    suspension_indicator = tonalanalysistools.Suspension('b2-1')
    assert suspension_indicator.start == tonalanalysistools.ScaleDegree('flat', 2)
    assert suspension_indicator.stop == tonalanalysistools.ScaleDegree(1)
