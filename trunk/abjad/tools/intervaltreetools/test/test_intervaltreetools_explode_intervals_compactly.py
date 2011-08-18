from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction
import py.test


def test_intervaltreetools_explode_intervals_compactly_01():
    '''Number of resulting trees is equal to the maximum depth of the source tree.'''
    tree = IntervalTree(_make_test_intervals())
    dtree = compute_depth_of_intervals(tree)
    xtrees = explode_intervals_compactly(tree)
    assert len(xtrees) == max([interval['depth'] for interval in dtree])

def test_intervaltreetools_explode_intervals_compactly_02():
    '''All resulting trees are non-zero in length.'''
    tree = IntervalTree(_make_test_intervals())
    xtrees = explode_intervals_compactly(tree)
    assert all([len(xtree) for xtree in xtrees])

def test_intervaltreetools_explode_intervals_compactly_03():
    '''All intervals in the source tree appear in the resulting trees once and only once.'''
    tree = IntervalTree(_make_test_intervals())
    xtrees = explode_intervals_compactly(tree)
    collapsed_tree = IntervalTree(xtrees)
    assert tree[:] == collapsed_tree[:]
