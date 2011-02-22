import py.test
from fractions import Fraction
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_explode_tree_compactly_01( ):
    '''Number of resulting trees is equal to the maximum depth of the source tree.'''
    tree = IntervalTree(_make_test_blocks( ))
    dtree = compute_depth_of_intervals(tree)
    xtrees = explode_tree_compactly(tree)
    assert len(xtrees) == max([interval.data['depth'] for interval in dtree])

def test_treetools_explode_tree_compactly_02( ):
    '''All resulting trees are non-zero in length.'''
    tree = IntervalTree(_make_test_blocks( ))
    xtrees = explode_tree_compactly(tree)
    assert all([len(xtree) for xtree in xtrees])

def test_treetools_explode_tree_compactly_03( ):
    '''All intervals in the source tree appear in the resulting trees once and only once.'''
    tree = IntervalTree(_make_test_blocks( ))
    xtrees = explode_tree_compactly(tree)
    collapsed_tree = IntervalTree(xtrees)
    assert tree.inorder == collapsed_tree.inorder   
