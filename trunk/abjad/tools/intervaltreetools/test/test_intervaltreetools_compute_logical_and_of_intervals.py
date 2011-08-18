from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
import py.test


def test_intervaltreetools_compute_logical_and_of_intervals_01():
    tree = IntervalTree(_make_test_intervals())
    logical_and = compute_logical_and_of_intervals(tree)
    target_signatures = [(6, 8), (8, 9), (9, 10), (16, 17),
        (17, 19), (19, 20), (20, 21), (26, 29)]
    actual_signatures = [interval.signature for interval in logical_and]
    assert actual_signatures == target_signatures

def test_intervaltreetools_compute_logical_and_of_intervals_02():
    tree = IntervalTree(BoundedInterval(5, 10))
    logical_and = compute_logical_and_of_intervals(tree)
    assert not len(logical_and)
