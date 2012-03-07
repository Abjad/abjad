from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
import py.test


def test_timeintervaltools_compute_logical_xor_of_intervals_01():
    tree = TimeIntervalTree(_make_test_intervals())
    logical_xor = compute_logical_xor_of_intervals(tree)
    target_signatures = [(0, 3), (5, 6), (10, 13), (15, 16), (21, 23), (25, 26), (29, 30), (32, 34), (34, 37)]
    actual_signatures = [interval.signature for interval in logical_xor]
    assert actual_signatures == target_signatures

def test_timeintervaltools_compute_logical_xor_of_intervals_02():
    tree = TimeIntervalTree(TimeInterval(5, 10))
    logical_xor = compute_logical_xor_of_intervals(tree)
    assert len(logical_xor) == len(tree)
    assert logical_xor[0].signature == tree[0].signature
