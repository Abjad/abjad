# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_timeintervaltools_TimeIntervalTree_scale_interval_durations_to_rational_01():
    time_interval_1 = timeintervaltools.TimeInterval(0, 10, {'time_interval_1': 1})
    time_interval_2 = timeintervaltools.TimeInterval(Fraction(5, 3), 10, {'time_interval_2': 2})
    time_interval_3 = timeintervaltools.TimeInterval(5, Fraction(61, 7), {'time_interval_3': 3})
    tree = timeintervaltools.TimeIntervalTree([time_interval_1, time_interval_2, time_interval_3])
    scalar = Fraction(5, 2)
    scaled = tree.scale_interval_durations_to_rational(scalar)
    assert scaled == timeintervaltools.TimeIntervalTree([
        timeintervaltools.TimeInterval(Offset(0, 1), Offset(5, 2), {'time_interval_1': 1}),
        timeintervaltools.TimeInterval(Offset(5, 3), Offset(25, 6), {'time_interval_2': 2}),
        timeintervaltools.TimeInterval(Offset(5, 1), Offset(15, 2), {'time_interval_3': 3})
        ])

def test_timeintervaltools_TimeIntervalTree_scale_interval_durations_to_rational_02():
    tree = timeintervaltools.TimeIntervalTree([])
    scalar = Fraction(5, 2)
    scaled = tree.scale_interval_durations_by_rational(scalar)
    assert scaled == tree
