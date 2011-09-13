from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
import py.test


def test_intervaltreetools_compute_logical_or_of_intervals_01():
    tree = IntervalTree(_make_test_intervals())
    logical_or = compute_logical_or_of_intervals(tree)
    target_signatures = [(0, 3), (5, 6), (6, 8), (8, 9), (9, 10),
        (10, 13), (15, 16), (16, 17), (17, 19),
        (19, 20), (20, 21), (21, 23), (25, 26),
        (26, 29), (29, 30), (32, 34), (34, 37)]
    actual_signatures = [interval.signature for interval in logical_or]
    assert actual_signatures == target_signatures

def test_intervaltreetools_compute_logical_or_of_intervals_02():
    tree = IntervalTree(BoundedInterval(5, 10))
    logical_or = compute_logical_or_of_intervals(tree)
    assert len(logical_or) == len(tree)
    assert logical_or[0].signature == tree[0].signature
