import py.test
from abjad.tools.treetools import IntervalTree
from abjad.tools.treetools import compute_logical_and_of_tree_or_trees
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_compute_logical_and_of_tree_or_trees_01( ):
    tree = IntervalTree(_make_test_blocks( ))
    logical_and = compute_logical_and_of_tree_or_trees(tree)
    target_signatures = [(6, 10), (16, 21), (26, 29)]
    actual_signatures = [interval.signature for interval in logical_and]
    assert actual_signatures == target_signatures
