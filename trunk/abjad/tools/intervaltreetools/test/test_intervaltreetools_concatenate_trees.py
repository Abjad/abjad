from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction
import py.test


def test_intervaltreetools_concatenate_trees_01():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    c = BoundedInterval(10, 20)
    tree_a = IntervalTree([a, b, c])
    tree_b = IntervalTree([a, b, c])
    concatenated = concatenate_trees([tree_a, tree_b])

    target_signatures = [(0, 10), (5, 15), (10, 20), (20, 30), (25, 35), (30, 40)]
    actual_signatures = [interval.signature for interval in concatenated]

    assert actual_signatures == target_signatures
    assert concatenated.magnitude == tree_a.magnitude + tree_b.magnitude
    assert a.signature == (0, 10)
    assert b.signature == (5, 15)
    assert c.signature == (10, 20)

def test_intervaltreetools_concatenate_trees_02():
    a = BoundedInterval(0, 10)
    b = BoundedInterval(5, 15)
    c = BoundedInterval(10, 20)
    tree_a = IntervalTree([a, b, c])
    tree_b = IntervalTree([a, b, c])
    concatenated = concatenate_trees([tree_a, tree_b], padding = Fraction(1, 2))

    target_signatures =  [(0, 10), (5, 15), (10, 20), \
                          (Fraction(41, 2), Fraction(61, 2)), (Fraction(51, 2),
                          Fraction(71, 2)), (Fraction(61, 2), Fraction(81, 2))]
    actual_signatures = [interval.signature for interval in concatenated]

    assert actual_signatures == target_signatures
    assert concatenated.magnitude == tree_a.magnitude + tree_b.magnitude + Fraction(1, 2)
