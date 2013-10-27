# -*- encoding: utf-8 -*-
from abjad import *


def test_timeintervaltools_TimeIntervalTree_calculate_mean_release_offset_01():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    mean_release_offset = tree.calculate_mean_release_offset() 
    assert mean_release_offset == Offset(
        sum(x.stop_offset for x in tree), len(tree))


def test_timeintervaltools_TimeIntervalTree_calculate_mean_release_offset_02():
    tree = timeintervaltools.TimeIntervalTree([])
    mean_release_offset = tree.calculate_mean_release_offset()
    assert mean_release_offset is None
