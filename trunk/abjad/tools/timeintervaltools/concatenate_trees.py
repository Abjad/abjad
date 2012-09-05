from abjad.tools import durationtools


def concatenate_trees(trees, padding=0):
    '''Merge all trees in `trees`, offsetting each subsequent tree
    to start after the previous.

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    assert all([isinstance(tree, timeintervaltools.TimeIntervalTree) for tree in trees])
    padding = durationtools.Duration(padding)
    assert 0 <= padding

    output_tree = timeintervaltools.TimeIntervalTree(
        timeintervaltools.shift_aggregate_offset_to_rational(trees[0], 0))
    for tree in trees[1:]:
        output_tree = timeintervaltools.TimeIntervalTree([
            output_tree,
            timeintervaltools.shift_aggregate_offset_to_rational(
                tree, output_tree.latest_stop + padding)
        ])

    return output_tree
