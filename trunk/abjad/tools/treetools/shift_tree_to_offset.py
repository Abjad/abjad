from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree


def shift_tree_to_offset(tree, value):
    '''Shift the start offset of all intervals in `tree` such that
    `tree.low` is equal to `value`.'''

    assert isinstance(tree, IntervalTree)
    assert isinstance(value, (int, Fraction))

    if tree.low_min == value:
        return tree
    else:
        shift = value - tree.low_min
        return IntervalTree([interval.shift_by_value(shift) \
                             for interval in tree])
