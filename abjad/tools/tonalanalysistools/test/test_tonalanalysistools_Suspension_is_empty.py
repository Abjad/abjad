# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Suspension_is_empty_01():

    suspension_indicator = tonalanalysistools.Suspension()

    assert suspension_indicator.is_empty
