from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
from fractions import Fraction
import py.test


def test_timeintervaltools_scale_interval_durations_by_rational_01():
    a = TimeInterval(0, 10, {'a': 1})
    b = TimeInterval(Fraction(5, 3), 10, {'b': 2})
    c = TimeInterval(5, 10, {'c': 3})
    tree = TimeIntervalTree([a, b, c])
    scalar = Fraction(5, 2)
    scaled = scale_interval_durations_by_rational(tree, scalar)
    assert scaled[0] == TimeInterval(0, Fraction(25, 1), {'a': 1})
    assert scaled[1] == TimeInterval(Fraction(5, 3), Fraction(45, 2), {'b': 2})
    assert scaled[2] == TimeInterval(5, Fraction(35, 2), {'c': 3})
    assert scaled.duration == (scalar * tree.duration)


def test_timeintervaltools_scale_interval_durations_by_rational_02():
    tree = TimeIntervalTree([])
    scalar = Fraction(5, 2)
    scaled = scale_interval_durations_by_rational(tree, scalar)
    assert scaled == tree
