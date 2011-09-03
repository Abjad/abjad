from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction
import py.test


def test_intervaltreetools_scale_interval_magnitudes_by_rational_01():
    a = BoundedInterval(0, 10, {'a': 1})
    b = BoundedInterval(Fraction(5, 3), 10, {'b': 2})
    c = BoundedInterval(5, 10, {'c': 3})
    tree = IntervalTree([a, b, c])
    scalar = Fraction(5, 2)
    scaled = scale_interval_magnitudes_by_rational(tree, scalar)
    assert scaled[0] == BoundedInterval(0, Fraction(25, 1), {'a': 1})
    assert scaled[1] == BoundedInterval(Fraction(5, 3), Fraction(45, 2), {'b': 2})
    assert scaled[2] == BoundedInterval(5, Fraction(35, 2), {'c': 3})
    assert scaled.magnitude == (scalar * tree.magnitude)


def test_intervaltreetools_scale_interval_magnitudes_by_rational_02():
    tree = IntervalTree([])
    scalar = Fraction(5, 2)
    scaled = scale_interval_magnitudes_by_rational(tree, scalar)
    assert scaled == tree
