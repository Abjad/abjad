# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Suspension__init_by_start_and_stop_01():

    suspension_indicator = tonalanalysistools.Suspension(4, 3)

    assert suspension_indicator.start == tonalanalysistools.ScaleDegree(4)
    assert suspension_indicator.stop == tonalanalysistools.ScaleDegree(3)


def test_tonalanalysistools_Suspension__init_by_start_and_stop_02():

    suspension_indicator = tonalanalysistools.Suspension(4, ('flat', 3))

    assert suspension_indicator.start == tonalanalysistools.ScaleDegree(4)
    assert suspension_indicator.stop == tonalanalysistools.ScaleDegree('flat', 3)
