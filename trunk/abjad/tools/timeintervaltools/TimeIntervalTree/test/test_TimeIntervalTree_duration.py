# -*- encoding: utf-8 -*-
from abjad.tools.timeintervaltools import *
import py.test


def test_TimeIntervalTree_duration_01():
    time_interval_1 = TimeInterval(-1, 2)
    time_interval_2 = TimeInterval(0, 1)
    time_interval_3 = TimeInterval(1, 3)

    tree = TimeIntervalTree(time_interval_1)
    assert tree.duration == 3

    tree = TimeIntervalTree(time_interval_2)
    assert tree.duration == 1

    tree = TimeIntervalTree(time_interval_3)
    assert tree.duration == 2

    tree = TimeIntervalTree([time_interval_1, time_interval_2])
    assert tree.duration == 3

    tree = TimeIntervalTree([time_interval_1, time_interval_3])
    assert tree.duration == 4

    tree = TimeIntervalTree([time_interval_2, time_interval_3])
    assert tree.duration == 3

    tree = TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    assert tree.duration == 4
