# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *
import py.test


def test_timeintervaltools_concatenate_trees_01():
    time_interval_1 = TimeInterval(0, 10)
    time_interval_2 = TimeInterval(5, 15)
    time_interval_3 = TimeInterval(10, 20)
    tree_a = TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    tree_b = TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    concatenated = concatenate_trees([tree_a, tree_b])

    target_signatures = [(0, 10), (5, 15), (10, 20), (20, 30), (25, 35), (30, 40)]
    actual_signatures = [interval.signature for interval in concatenated]

    assert actual_signatures == target_signatures
    assert concatenated.duration == tree_a.duration + tree_b.duration
    assert time_interval_1.signature == (0, 10)
    assert time_interval_2.signature == (5, 15)
    assert time_interval_3.signature == (10, 20)

def test_timeintervaltools_concatenate_trees_02():
    time_interval_1 = TimeInterval(0, 10)
    time_interval_2 = TimeInterval(5, 15)
    time_interval_3 = TimeInterval(10, 20)
    tree_a = TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    tree_b = TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    concatenated = concatenate_trees([tree_a, tree_b], padding=Fraction(1, 2))

    target_signatures =  [(0, 10), (5, 15), (10, 20), \
                          (Fraction(41, 2), Fraction(61, 2)), (Fraction(51, 2),
                          Fraction(71, 2)), (Fraction(61, 2), Fraction(81, 2))]
    actual_signatures = [interval.signature for interval in concatenated]

    assert actual_signatures == target_signatures
    assert concatenated.duration == tree_a.duration + tree_b.duration + Fraction(1, 2)
