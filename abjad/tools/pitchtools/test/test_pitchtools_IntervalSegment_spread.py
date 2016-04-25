# -*- coding: utf-8 -*-
from abjad.tools.pitchtools import NumberedInterval
from abjad.tools.pitchtools import IntervalSegment


def test_pitchtools_IntervalSegment_spread_01():
    mcis = IntervalSegment([1, 2, -3, 1, -2, 1])
    assert mcis.spread == NumberedInterval(4)


def test_pitchtools_IntervalSegment_spread_02():
    mcis = IntervalSegment([1, 1, 1, 2, -3, -2])
    assert mcis.spread == NumberedInterval(5)


def test_pitchtools_IntervalSegment_spread_03():
    mcis = IntervalSegment([1, 1, -2, 2, -3, 1])
    assert mcis.spread == NumberedInterval(3)
