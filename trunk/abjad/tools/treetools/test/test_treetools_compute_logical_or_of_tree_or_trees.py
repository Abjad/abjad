import py.test
from abjad.tools.treetools import IntervalTree
from abjad.tools.treetools import compute_logical_or_of_tree_or_trees
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_compute_logical_or_of_tree_or_trees_01( ):
    tree = IntervalTree(_make_test_blocks( ))
    logical_or = compute_logical_or_of_tree_or_trees(tree)
    target_signatures = [(0, 3), (5, 13), (15, 23), (25, 30), (32, 37)]
    actual_signatures = [interval.signature for interval in logical_or]
    assert actual_signatures == target_signatures
