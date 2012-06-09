from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools._make_test_intervals import _make_test_intervals
from fractions import Fraction
import py.test


def test_timeintervaltools_explode_intervals_uncompactly_01():
    '''Number of resulting trees is equal to the maximum depth of the source tree.'''
    tree = TimeIntervalTree(_make_test_intervals())
    dtree = compute_depth_of_intervals(tree)
    xtrees = explode_intervals_uncompactly(tree)
    assert len(xtrees) == max([interval['depth'] for interval in dtree])

def test_timeintervaltools_explode_intervals_uncompactly_02():
    '''All resulting trees are non-zero in length.'''
    tree = TimeIntervalTree(_make_test_intervals())
    xtrees = explode_intervals_uncompactly(tree)
    assert all([len(xtree) for xtree in xtrees])

def test_timeintervaltools_explode_intervals_uncompactly_03():
    '''All intervals in the source tree appear in the resulting trees once and only once.'''
    tree = TimeIntervalTree(_make_test_intervals())
    xtrees = explode_intervals_uncompactly(tree)
    collapsed_tree = TimeIntervalTree(xtrees)
    assert tree[:] == collapsed_tree[:]
