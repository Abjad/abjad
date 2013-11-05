# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_timeintervaltools_TimeIntervalTree_intervals_are_contiguous_01():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(10, 20)
    time_interval_3 = timeintervaltools.TimeInterval(20, 30)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    assert tree.intervals_are_contiguous


def test_timeintervaltools_TimeIntervalTree_intervals_are_contiguous_02():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(5, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2])
    assert not tree.intervals_are_contiguous


def test_timeintervaltools_TimeIntervalTree_intervals_are_contiguous_03():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(15, 25)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2])
    assert not tree.intervals_are_contiguous
