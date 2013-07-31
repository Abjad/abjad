# -*- encoding: utf-8 -*-
from abjad.tools import durationtools


def concatenate_trees(trees, padding=0):
    r'''Merge all trees in `trees`, offsetting each subsequent tree
    to start_offset after the previous.

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    assert all(isinstance(tree, timeintervaltools.TimeIntervalTree) for tree in trees)
    padding = durationtools.Duration(padding)
    assert 0 <= padding

    output_tree = trees[0].shift_to_rational(0)
    for tree in trees[1:]:
        output_tree = timeintervaltools.TimeIntervalTree([
            output_tree,
            tree.shift_to_rational(output_tree.latest_stop + padding)
        ])

    return output_tree
