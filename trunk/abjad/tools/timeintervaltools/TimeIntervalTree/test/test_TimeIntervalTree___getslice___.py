# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *


def test_TimeIntervalTree___getslice____01():
    intervals = timeintervaltools.make_test_intervals()
    tree = TimeIntervalTree(intervals)
    assert tuple(intervals[:]) == tree[:]
    assert tuple(intervals[:2]) == tree[:2]
    assert tuple(intervals[-2:]) == tree[-2:]
    assert tuple(intervals[1:3]) == tree[1:3]
