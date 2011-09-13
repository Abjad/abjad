from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction
import py.test


def test_intervaltreetools_split_intervals_at_rationals_01():
    splits = [-1, 16]
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    tree = IntervalTree([a, b])
    split = split_intervals_at_rationals(tree, splits)
    assert tree[:] == split[:]
