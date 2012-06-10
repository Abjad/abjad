from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
from fractions import Fraction
import py.test


def test_timeintervaltools_concatenate_trees_01():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    c = TimeInterval(10, 20)
    tree_a = TimeIntervalTree([a, b, c])
    tree_b = TimeIntervalTree([a, b, c])
    concatenated = concatenate_trees([tree_a, tree_b])

    target_signatures = [(0, 10), (5, 15), (10, 20), (20, 30), (25, 35), (30, 40)]
    actual_signatures = [interval.signature for interval in concatenated]

    assert actual_signatures == target_signatures
    assert concatenated.duration == tree_a.duration + tree_b.duration
    assert a.signature == (0, 10)
    assert b.signature == (5, 15)
    assert c.signature == (10, 20)

def test_timeintervaltools_concatenate_trees_02():
    a = TimeInterval(0, 10)
    b = TimeInterval(5, 15)
    c = TimeInterval(10, 20)
    tree_a = TimeIntervalTree([a, b, c])
    tree_b = TimeIntervalTree([a, b, c])
    concatenated = concatenate_trees([tree_a, tree_b], padding=Fraction(1, 2))

    target_signatures =  [(0, 10), (5, 15), (10, 20), \
                          (Fraction(41, 2), Fraction(61, 2)), (Fraction(51, 2),
                          Fraction(71, 2)), (Fraction(61, 2), Fraction(81, 2))]
    actual_signatures = [interval.signature for interval in concatenated]

    assert actual_signatures == target_signatures
    assert concatenated.duration == tree_a.duration + tree_b.duration + Fraction(1, 2)
