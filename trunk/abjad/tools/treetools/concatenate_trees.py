from fractions import Fraction
from abjad.tools.treetools import *


def concatenate_trees(trees, padding = 0):
    assert all([isinstance(tree, IntervalTree) for tree in trees])
    assert isinstance(padding, (int, Fraction))
    print 'not yet implemented.'
