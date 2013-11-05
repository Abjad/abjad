# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_timeintervaltools_TimeIntervalTree_intervals_are_nonoverlapping_01():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(10, 20)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2])
    assert tree.intervals_are_nonoverlapping


def test_timeintervaltools_TimeIntervalTree_intervals_are_nonoverlapping_02():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(5, 15)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2])
    assert not tree.intervals_are_nonoverlapping


def test_timeintervaltools_TimeIntervalTree_intervals_are_nonoverlapping_03():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10)
    time_interval_2 = timeintervaltools.TimeInterval(15, 25)
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2])
    assert tree.intervals_are_nonoverlapping
