import py.test
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_compute_logical_and_of_intervals_01( ):
    tree = IntervalTree(_make_test_blocks( ))
    logical_and = compute_logical_and_of_intervals(tree)
    target_signatures = [(6, 10), (16, 21), (26, 29)]
    actual_signatures = [interval.signature for interval in logical_and]
    assert actual_signatures == target_signatures

def test_treetools_compute_logical_and_of_intervals_02( ):
    tree = IntervalTree(BoundedInterval(5, 10))
    logical_and = compute_logical_and_of_intervals(tree)
    assert not len(logical_and)
