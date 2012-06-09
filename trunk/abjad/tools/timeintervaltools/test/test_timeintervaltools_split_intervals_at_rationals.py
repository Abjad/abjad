from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
from fractions import Fraction
import py.test


def test_timeintervaltools_split_intervals_at_rationals_01():
    splits = [-1, 16]
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    tree = TimeIntervalTree([a, b])
    split = split_intervals_at_rationals(tree, splits)
    assert tree[:] == split[:]
