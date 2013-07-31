# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_TimeIntervalTree_scale_interval_durations_by_rational_01():
    a = timeintervaltools.TimeInterval(0, 10, {'a': 1})
    b = timeintervaltools.TimeInterval(Fraction(5, 3), 10, {'b': 2})
    c = timeintervaltools.TimeInterval(5, 10, {'c': 3})
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    scalar = Fraction(5, 2)
    scaled = tree.scale_interval_durations_by_rational(scalar)
    assert scaled[0] == timeintervaltools.TimeInterval(0, Fraction(25, 1), {'a': 1})
    assert scaled[1] == timeintervaltools.TimeInterval(Fraction(5, 3), Fraction(45, 2), {'b': 2})
    assert scaled[2] == timeintervaltools.TimeInterval(5, Fraction(35, 2), {'c': 3})
    assert scaled.duration == (scalar * tree.duration)


def test_TimeIntervalTree_scale_interval_durations_by_rational_02():
    tree = timeintervaltools.TimeIntervalTree([])
    scalar = Fraction(5, 2)
    scaled = tree.scale_interval_durations_by_rational(scalar)
    assert scaled == tree
