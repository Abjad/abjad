from fractions import Fraction
from abjad.tools.treetools.IntervalTree import IntervalTree


def shift_tree_by_offset(tree, value):
    '''Shift the start offset of all intervals in `tree` by `value`.'''

    assert isinstance(tree, IntervalTree)
    assert isinstance(value, (int, Fraction))

    if value == 0:
        return tree
    else:
        return IntervalTree([interval.shift_by_value(value) \
                             for interval in tree])
