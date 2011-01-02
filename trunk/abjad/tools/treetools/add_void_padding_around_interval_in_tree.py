from abjad.tools.treetools import *


def _add_void_padding_around_interval_in_tree(tree, interval, pad_before = 0, pad_after = 0):
    '''Create empty space around an interval, 
    clipping other intervals which intersect it or its padding.'''

    assert isinstance(tree, IntervalTree)
    assert isinstance(interval, BoundedInterval)
    assert all([isinstance(pad, (int, Fraction)) for pad in [pad_before, pad_after]])
    print 'not yet implemented.'
