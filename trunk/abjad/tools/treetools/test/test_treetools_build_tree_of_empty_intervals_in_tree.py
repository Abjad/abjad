from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools import build_tree_of_empty_intervals_in_tree
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_build_tree_of_empty_intervals_in_tree_01( ):
    tree = IntervalTree(_make_test_blocks( ))
    empties = build_tree_of_empty_intervals_in_tree(tree)
    target_signatures = [(3, 5), (13, 15), (23, 25), (30, 32)]
    actual_signatures = map(lambda x: x.signature, empties)
    assert actual_signatures == target_signatures
