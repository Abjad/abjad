# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_timeintervaltools_TimeIntervalTree_scale_interval_durations_by_rational_01():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10, {'time_interval_1': 1})
    time_interval_2 = timeintervaltools.TimeInterval(Fraction(5, 3), 10, {'time_interval_2': 2})
    time_interval_3 = timeintervaltools.TimeInterval(5, 10, {'time_interval_3': 3})
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    scalar = Fraction(5, 2)
    scaled = tree.scale_interval_durations_by_rational(scalar)
    assert scaled[0] == timeintervaltools.TimeInterval(0, Fraction(25, 1), {'time_interval_1': 1})
    assert scaled[1] == timeintervaltools.TimeInterval(Fraction(5, 3), Fraction(45, 2), {'time_interval_2': 2})
    assert scaled[2] == timeintervaltools.TimeInterval(5, Fraction(35, 2), {'time_interval_3': 3})
    assert scaled.duration == (scalar * tree.duration)


def test_timeintervaltools_TimeIntervalTree_scale_interval_durations_by_rational_02():
    tree = timeintervaltools.TimeIntervalTree([])
    scalar = Fraction(5, 2)
    scaled = tree.scale_interval_durations_by_rational(scalar)
    assert scaled == tree
