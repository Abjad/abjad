import py.test
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


py.test.skip('Awaiting rewrite of IntervalTree backend.')

def test_IntervalTree_shift_member_interval_to_value_01( ):
    '''Altered intervals are replaced in the tree.'''
    tree = IntervalTree(_make_test_blocks( ))
    old = tree.find_intervals_starting_at_offset(8)
    assert len(old) == 1
    tree.shift_member_interval_to_value(old[0], -100)
    new = tree.find_intervals_starting_at_offset(-100)
    assert len(new) == 1
    assert old != new
    assert old[0] not in tree

def test_IntervalTree_shift_member_interval_to_value_02( ):
    '''Non-member intervals cannot be altered.'''
    tree = IntervalTree(_make_test_blocks( ))
    nonmember = Block(-3, 2, 'non-member')
    py.test.raises(AssertionError,
        'tree.shift_member_interval_to_value(nonmember, 3)')

