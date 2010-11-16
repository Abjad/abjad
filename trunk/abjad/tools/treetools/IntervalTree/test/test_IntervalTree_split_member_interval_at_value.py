import py.test
from fractions import Fraction
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


#py.test.skip('Awaiting rewrite of IntervalTree backend.')

def test_IntervalTree_split_member_interval_at_value_01( ):
    '''Altered intervals are replaced in the tree.'''
    tree = IntervalTree(_make_test_blocks( ))
    old = tree.find_intervals_starting_at_offset(0)
    assert len(old) == 1
    splits = tree.split_member_interval_at_value(old[0], Fraction(3, 2))
    new = tree.find_intervals_starting_at_offset(0)
    assert len(splits) == 2
    assert old != new
    assert splits[0] in tree and splits[1] in tree and old not in tree

def test_IntervalTree_split_member_interval_at_value_02( ):
    '''Non-member intervals cannot be altered.'''
    tree = IntervalTree(_make_test_blocks( ))
    nonmember = Block(-3, 20, 'non-member')
    py.test.raises(AssertionError,
        'tree.split_member_interval_at_value(nonmember, 3)')

