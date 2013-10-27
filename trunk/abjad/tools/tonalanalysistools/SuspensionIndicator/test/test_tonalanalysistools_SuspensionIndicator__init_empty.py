# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_SuspensionIndicator__init_empty_01():

    suspension_indicator = tonalanalysistools.SuspensionIndicator()

    assert suspension_indicator.start is None
    assert suspension_indicator.stop is None
