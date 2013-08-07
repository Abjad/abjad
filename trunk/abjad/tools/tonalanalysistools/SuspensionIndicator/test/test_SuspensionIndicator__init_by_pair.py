# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_SuspensionIndicator__init_by_pair_01():

    suspension_indicator = tonalanalysistools.SuspensionIndicator((4, 3))

    assert suspension_indicator.start == tonalanalysistools.ScaleDegree(4)
    assert suspension_indicator.stop == tonalanalysistools.ScaleDegree(3)
