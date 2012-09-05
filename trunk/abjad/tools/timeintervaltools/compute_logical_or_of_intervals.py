def compute_logical_or_of_intervals(intervals):
    '''Compute the logical OR of a collection of intervals.

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return tree

    depth_tree = timeintervaltools.compute_depth_of_intervals(tree)
    logic_tree = timeintervaltools.TimeIntervalTree([x for x in depth_tree if 1 <= x['depth']])

    return logic_tree
