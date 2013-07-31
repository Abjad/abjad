# -*- encoding: utf-8 -*-
from abjad import *


def test_TimeIntervalTree_all_unique_bounds_01():
    tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.make_test_intervals())
    target_bounds = (0, 3, 5, 6, 8, 9, 10, 13, 15, 16, 17, 19, 20, 21, 23, 25, 26, 29, 30, 32, 34, 37)
    actual_bounds = tree.all_unique_bounds
    assert actual_bounds == target_bounds


def test_TimeIntervalTree_all_unique_bounds_02():
    tree = timeintervaltools.TimeIntervalTree([])
    target_bounds = ()
    actual_bounds = tree.all_unique_bounds
    assert actual_bounds == target_bounds
