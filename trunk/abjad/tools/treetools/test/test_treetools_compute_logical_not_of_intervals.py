import py.test
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_compute_logical_not_of_intervals_01( ):
    tree = IntervalTree(_make_test_blocks( ))
    logical_not = compute_logical_not_of_intervals(tree)
    target_signatures = [(3, 5), (13, 15), (23, 25), (30, 32)]
    actual_signatures = [interval.signature for interval in logical_not]
    assert actual_signatures == target_signatures

def test_treetools_compute_logical_not_of_intervals_02( ):
    tree = IntervalTree(BoundedInterval(5, 10))
    logical_not = compute_logical_not_of_intervals(tree)
    assert not len(logical_not)
