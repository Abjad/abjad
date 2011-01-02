import py.test
from fractions import Fraction
from abjad.tools.treetools import *
from abjad.tools.treetools._make_test_blocks import _make_test_blocks 


def test_treetools_split_intervals_in_tree_at_values_01( ):

    a = BoundedInterval(0, 15)
    b = BoundedInterval(5, 20)
    c = BoundedInterval(10, 25)
    tree = IntervalTree([a, b, c])
    split_values = [-1, 5, 6, 15, Fraction(31, 2), 26]
    split_tree = split_intervals_in_tree_at_values(tree, split_values)

    target_signatures = [(0, 5), (5, 6), (5, 6), (6, 15), (6, 15), (10, 15), 
                         (15, Fraction(31, 2)), (15, Fraction(31, 2)), 
                         (Fraction(31, 2), 20), (Fraction(31, 2), 25)]
    actual_signatures = [interval.signature for interval in split_tree]

    assert actual_signatures == target_signatures
    assert split_tree.magnitude == tree.magnitude

