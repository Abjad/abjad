import py.test
from abjad.tools.treetools import IntervalTree
from abjad.tools.treetools import compute_logical_xor_of_intervals
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_compute_logical_xor_of_intervals_01( ):
    tree = IntervalTree(_make_test_blocks( ))
    logical_xor = compute_logical_xor_of_intervals(tree)
    target_signatures = [(0, 3), (5, 6), (10, 13), (15, 16), (21, 23), (25, 26), (29, 30), (32, 37)]
    actual_signatures = [interval.signature for interval in logical_xor]
    assert actual_signatures == target_signatures
