# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Suspension__init_empty_01():

    suspension_indicator = tonalanalysistools.Suspension()

    assert suspension_indicator.start is None
    assert suspension_indicator.stop is None
