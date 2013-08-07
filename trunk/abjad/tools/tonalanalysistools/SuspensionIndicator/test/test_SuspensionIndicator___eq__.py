# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_SuspensionIndicator___eq___01():

    suspension_indicator = tonalanalysistools.SuspensionIndicator(4, 3)
    u = tonalanalysistools.SuspensionIndicator(4, 3)
    v = tonalanalysistools.SuspensionIndicator(2, 1)

    assert      suspension_indicator == suspension_indicator
    assert      suspension_indicator == u
    assert not suspension_indicator == v

    assert      u == suspension_indicator
    assert      u == u
    assert not u == v

    assert not v == suspension_indicator
    assert not v == u
    assert      v == v
