# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedMelodicIntervalSegment_slope_01():
    mcis = pitchtools.NumberedMelodicIntervalSegment([1])
    assert mcis.slope == 1


def test_NumberedMelodicIntervalSegment_slope_02():
    mcis = pitchtools.NumberedMelodicIntervalSegment([-2, 1])
    assert mcis.slope == Fraction(-1, 2)


def test_NumberedMelodicIntervalSegment_slope_03():
    mcis = pitchtools.NumberedMelodicIntervalSegment([1, 2, -3, 0, 2, -1, -1.5, 0.5])
    assert mcis.slope == 0
