from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
from fractions import Fraction
import py.test


def test_timeintervaltools_round_interval_bounds_to_nearest_multiple_of_rational_01():
    tree = TimeIntervalTree([
        TimeInterval(Fraction(1, 4), Fraction(7, 8)),
        TimeInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    result = round_interval_bounds_to_nearest_multiple_of_rational(tree, 1)
    assert result == \
    TimeIntervalTree([
        TimeInterval(Fraction(0, 1), Fraction(1, 1), {}),
        TimeInterval(Fraction(0, 1), Fraction(2, 1), {})
    ])


def test_timeintervaltools_round_interval_bounds_to_nearest_multiple_of_rational_02():
    tree = TimeIntervalTree([
        TimeInterval(Fraction(1, 4), Fraction(7, 8)),
        TimeInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    result = round_interval_bounds_to_nearest_multiple_of_rational(tree, Fraction(1, 4))
    assert result == \
    TimeIntervalTree([
        TimeInterval(Fraction(1, 4), Fraction(1, 1), {}),
        TimeInterval(Fraction(1, 4), Fraction(7, 4), {})
    ])


def test_timeintervaltools_round_interval_bounds_to_nearest_multiple_of_rational_03():
    tree = TimeIntervalTree([
        TimeInterval(Fraction(1, 4), Fraction(7, 8)),
        TimeInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    result = round_interval_bounds_to_nearest_multiple_of_rational(tree, Fraction(2, 5))
    assert result == \
    TimeIntervalTree([
        TimeInterval(Fraction(2, 5), Fraction(4, 5), {}),
        TimeInterval(Fraction(2, 5), Fraction(8, 5), {})
    ])


def test_timeintervaltools_round_interval_bounds_to_nearest_multiple_of_rational_04():
    tree = TimeIntervalTree([
        TimeInterval(Fraction(1, 4), Fraction(7, 8)),
        TimeInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    py.test.raises(AssertionError, "result = round_interval_bounds_to_nearest_multiple_of_rational(tree, 0)")


def test_timeintervaltools_round_interval_bounds_to_nearest_multiple_of_rational_05():
    tree = TimeIntervalTree([])
    result = round_interval_bounds_to_nearest_multiple_of_rational(tree, 1)
    assert result == tree
