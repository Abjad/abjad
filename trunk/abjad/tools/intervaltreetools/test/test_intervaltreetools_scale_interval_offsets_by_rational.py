from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction
import py.test


def test_intervaltreetools_scale_interval_offsets_by_rational_01():
    a = BoundedInterval(0, 10, {'a': 1})
    b = BoundedInterval(Fraction(5, 3), 8, {'b': 2})
    c = BoundedInterval(5, Fraction(61, 7), {'c': 3})
    tree = IntervalTree([a, b, c])
    scalar = Fraction(5, 2)
    scaled = scale_interval_offsets_by_rational(tree, scalar)
    assert scaled[0] == BoundedInterval(0, 10, {'a': 1})
    assert scaled[1] == BoundedInterval(Fraction(25, 6), Fraction(21, 2), {'b': 2})
    assert scaled[2] == BoundedInterval(Fraction(25, 2), Fraction(227, 14), {'c': 3})
    assert scaled[0].duration == a.duration
    assert scaled[1].duration == b.duration
    assert scaled[2].duration == c.duration

def test_intervaltreetools_scale_interval_offsets_by_rational_02():
    tree = IntervalTree([])
    scalar = Fraction(5, 2)
    scaled = scale_interval_offsets_by_rational(tree, scalar)
    assert scaled == tree
