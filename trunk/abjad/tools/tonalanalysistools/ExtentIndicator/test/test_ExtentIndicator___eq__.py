# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_ExtentIndicator___eq___01():

    extentindicator = tonalanalysistools.ExtentIndicator(5)
    u = tonalanalysistools.ExtentIndicator(5)
    v = tonalanalysistools.ExtentIndicator(7)

    assert      extentindicator == extentindicator
    assert      extentindicator == u
    assert not extentindicator == v

    assert      u == extentindicator
    assert      u == u
    assert not u == v

    assert not v == extentindicator
    assert not v == u
    assert      v == v
