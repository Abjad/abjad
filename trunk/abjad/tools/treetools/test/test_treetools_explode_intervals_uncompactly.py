from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks
from abjad import Fraction
import py.test


def test_treetools_explode_intervals_uncompactly_01( ):
   '''Number of resulting trees is equal to the maximum depth of the source tree.'''
   tree = IntervalTree(_make_test_blocks( ))
   dtree = compute_depth_of_intervals(tree)
   xtrees = explode_intervals_uncompactly(tree)
   assert len(xtrees) == max([interval['depth'] for interval in dtree])

def test_treetools_explode_intervals_uncompactly_02( ):
   '''All resulting trees are non-zero in length.'''
   tree = IntervalTree(_make_test_blocks( ))
   xtrees = explode_intervals_uncompactly(tree)
   assert all([len(xtree) for xtree in xtrees])

def test_treetools_explode_intervals_uncompactly_03( ):
   '''All intervals in the source tree appear in the resulting trees once and only once.'''
   tree = IntervalTree(_make_test_blocks( ))
   xtrees = explode_intervals_uncompactly(tree)
   collapsed_tree = IntervalTree(xtrees)
   assert tree[:] == collapsed_tree[:]

