# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools import NumberedMelodicInterval
from abjad.tools.pitchtools import IntervalSegment


def test_IntervalSegment_spread_01():
    mcis = IntervalSegment([1, 2, -3, 1, -2, 1])
    assert mcis.spread == NumberedMelodicInterval(4)


def test_IntervalSegment_spread_02():
    mcis = IntervalSegment([1, 1, 1, 2, -3, -2])
    assert mcis.spread == NumberedMelodicInterval(5)


def test_IntervalSegment_spread_03():
    mcis = IntervalSegment([1, 1, -2, 2, -3, 1])
    assert mcis.spread == NumberedMelodicInterval(3)
