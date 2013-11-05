# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_TimeIntervalTree___getitem____01():
    intervals = timeintervaltools.make_test_intervals()
    tree = TimeIntervalTree(intervals)
    assert tree[0] == intervals[0]
    assert tree[1] == intervals[1]
    assert tree[-1] == intervals[-1]
    assert tree[-2] == intervals[-2]
