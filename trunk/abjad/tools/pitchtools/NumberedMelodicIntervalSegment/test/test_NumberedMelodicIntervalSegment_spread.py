# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools import NumberedHarmonicInterval
from abjad.tools.pitchtools import NumberedMelodicIntervalSegment


def test_NumberedMelodicIntervalSegment_spread_01():
    mcis = NumberedMelodicIntervalSegment([1, 2, -3, 1, -2, 1])
    assert mcis.spread == NumberedHarmonicInterval(4)


def test_NumberedMelodicIntervalSegment_spread_02():
    mcis = NumberedMelodicIntervalSegment([1, 1, 1, 2, -3, -2])
    assert mcis.spread == NumberedHarmonicInterval(5)


def test_NumberedMelodicIntervalSegment_spread_03():
    mcis = NumberedMelodicIntervalSegment([1, 1, -2, 2, -3, 1])
    assert mcis.spread == NumberedHarmonicInterval(3)
