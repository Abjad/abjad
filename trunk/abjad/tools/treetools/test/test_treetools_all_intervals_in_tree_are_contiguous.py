import py.test
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_all_intervals_in_tree_are_contiguous_01( ):
    tree = IntervalTree( )
    tree.insert(BoundedInterval(0, 10))
    tree.insert(BoundedInterval(10, 10))
    tree.insert(BoundedInterval(10, 20))
    tree.insert(BoundedInterval(20, 30))
    assert all_intervals_in_tree_are_contiguous(tree)

def test_treetools_all_intervals_in_tree_are_contiguous_02( ):
    tree = IntervalTree( )
    tree.insert(BoundedInterval(0, 10))
    tree.insert(BoundedInterval(5, 15))
    assert not all_intervals_in_tree_are_contiguous(tree)

def test_treetools_all_intervals_in_tree_are_contiguous_03( ):
    tree = IntervalTree( )
    tree.insert(BoundedInterval(0, 10))
    tree.insert(BoundedInterval(15, 25))
    assert not all_intervals_in_tree_are_contiguous(tree)
