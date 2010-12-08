from fractions import Fraction
from abjad.tools.treetools import *


def _split_intervals_in_tree_at_values(tree, values):
    assert isinstance(tree, IntervalTree)
    assert len(values)
    assert all([isinstance(x, (int, Fraction)) for x in values])
    print 'not yet implemented.'
