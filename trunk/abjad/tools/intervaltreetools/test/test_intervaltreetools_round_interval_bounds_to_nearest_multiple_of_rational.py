from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction
import py.test


def test_intervaltreetools_round_interval_bounds_to_nearest_multiple_of_rational_01():
    tree = IntervalTree([
        BoundedInterval(Fraction(1, 4), Fraction(7, 8)),
        BoundedInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    result = round_interval_bounds_to_nearest_multiple_of_rational(tree, 1)
    assert result == \
    IntervalTree([
        BoundedInterval(Fraction(0, 1), Fraction(1, 1), {}),
        BoundedInterval(Fraction(0, 1), Fraction(2, 1), {})
    ])


def test_intervaltreetools_round_interval_bounds_to_nearest_multiple_of_rational_02():
    tree = IntervalTree([
        BoundedInterval(Fraction(1, 4), Fraction(7, 8)),
        BoundedInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    result = round_interval_bounds_to_nearest_multiple_of_rational(tree, Fraction(1, 4))
    assert result == \
    IntervalTree([
        BoundedInterval(Fraction(1, 4), Fraction(1, 1), {}),
        BoundedInterval(Fraction(1, 4), Fraction(7, 4), {})
    ])


def test_intervaltreetools_round_interval_bounds_to_nearest_multiple_of_rational_03():
    tree = IntervalTree([
        BoundedInterval(Fraction(1, 4), Fraction(7, 8)),
        BoundedInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    result = round_interval_bounds_to_nearest_multiple_of_rational(tree, Fraction(2, 5))
    assert result == \
    IntervalTree([
        BoundedInterval(Fraction(2, 5), Fraction(4, 5), {}),
        BoundedInterval(Fraction(2, 5), Fraction(8, 5), {})
    ])


def test_intervaltreetools_round_interval_bounds_to_nearest_multiple_of_rational_04():
    tree = IntervalTree([
        BoundedInterval(Fraction(1, 4), Fraction(7, 8)),
        BoundedInterval(Fraction(1, 3), Fraction(5, 3))
    ])
    py.test.raises(AssertionError, "result = round_interval_bounds_to_nearest_multiple_of_rational(tree, 0)")


def test_intervaltreetools_round_interval_bounds_to_nearest_multiple_of_rational_05():
    tree = IntervalTree([])
    result = round_interval_bounds_to_nearest_multiple_of_rational(tree, 1)
    assert result == tree
