import py.test
from fractions import Fraction
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks


def test_treetools_mask_intervals_with_intervals_01( ):
    a = BoundedInterval(0, 9, 'a')
    b = BoundedInterval(6, 10, 'b')
    c = BoundedInterval(5, 10, 'c')
    masked = IntervalTree([a, b])
    mask = IntervalTree([c])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(5, 9), (6, 10)]
    actual_signatures = [interval.signature for interval in result.inorder]
    assert target_signatures == actual_signatures
    assert result.inorder[0].data == a.data
    assert result.inorder[1].data == b.data

def test_treetools_mask_intervals_with_intervals_02( ):
    a = BoundedInterval(0, 9, 'a')
    b = BoundedInterval(6, 10, 'b')
    c = BoundedInterval(5, 6, 'c')
    d = BoundedInterval(7, 8, 'd')
    masked = IntervalTree([a, b])
    mask = IntervalTree([c, d])
    result = mask_intervals_with_intervals(masked, mask)
    target_signatures = [(5, 6), (7, 8), (7, 8)]
    actual_signatures = [interval.signature for interval in result.inorder]
    assert target_signatures == actual_signatures
