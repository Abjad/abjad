# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_TimeIntervalTree_scale_interval_offsets_by_rational_01():
    a = timeintervaltools.TimeInterval(0, 10, {'a': 1})
    b = timeintervaltools.TimeInterval(Fraction(5, 3), 8, {'b': 2})
    c = timeintervaltools.TimeInterval(5, Fraction(61, 7), {'c': 3})
    tree = timeintervaltools.TimeIntervalTree([a, b, c])
    scalar = Fraction(5, 2)
    scaled = tree.scale_interval_offsets_by_rational(scalar)
    assert scaled[0] == timeintervaltools.TimeInterval(0, 10, {'a': 1})
    assert scaled[1] == timeintervaltools.TimeInterval(Fraction(25, 6), Fraction(21, 2), {'b': 2})
    assert scaled[2] == timeintervaltools.TimeInterval(Fraction(25, 2), Fraction(227, 14), {'c': 3})
    assert scaled[0].duration == a.duration
    assert scaled[1].duration == b.duration
    assert scaled[2].duration == c.duration

def test_TimeIntervalTree_scale_interval_offsets_by_rational_02():
    tree = timeintervaltools.TimeIntervalTree([])
    scalar = Fraction(5, 2)
    scaled = tree.scale_interval_offsets_by_rational(scalar)
    assert scaled == tree
