from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
import py.test


def test_timeintervaltools_compute_logical_and_of_intervals_01():
    tree = TimeIntervalTree(_make_test_intervals())
    logical_and = compute_logical_and_of_intervals(tree)
    target_signatures = [(6, 8), (8, 9), (9, 10), (16, 17),
        (17, 19), (19, 20), (20, 21), (26, 29)]
    actual_signatures = [interval.signature for interval in logical_and]
    assert actual_signatures == target_signatures

def test_timeintervaltools_compute_logical_and_of_intervals_02():
    tree = TimeIntervalTree(TimeInterval(5, 10))
    logical_and = compute_logical_and_of_intervals(tree)
    assert not len(logical_and)
