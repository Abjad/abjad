from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
from fractions import Fraction
import py.test


def test_timeintervaltools_scale_interval_offsets_by_rational_01():
    a = TimeInterval(0, 10, {'a': 1})
    b = TimeInterval(Fraction(5, 3), 8, {'b': 2})
    c = TimeInterval(5, Fraction(61, 7), {'c': 3})
    tree = TimeIntervalTree([a, b, c])
    scalar = Fraction(5, 2)
    scaled = scale_interval_offsets_by_rational(tree, scalar)
    assert scaled[0] == TimeInterval(0, 10, {'a': 1})
    assert scaled[1] == TimeInterval(Fraction(25, 6), Fraction(21, 2), {'b': 2})
    assert scaled[2] == TimeInterval(Fraction(25, 2), Fraction(227, 14), {'c': 3})
    assert scaled[0].duration == a.duration
    assert scaled[1].duration == b.duration
    assert scaled[2].duration == c.duration

def test_timeintervaltools_scale_interval_offsets_by_rational_02():
    tree = TimeIntervalTree([])
    scalar = Fraction(5, 2)
    scaled = scale_interval_offsets_by_rational(tree, scalar)
    assert scaled == tree
