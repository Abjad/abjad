# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_SuspensionIndicator__init_by_reference_01():

    suspension_indicator = tonalanalysistools.SuspensionIndicator(4, 3)
    u = tonalanalysistools.SuspensionIndicator(suspension_indicator)

    assert suspension_indicator is not u
    assert suspension_indicator == u
