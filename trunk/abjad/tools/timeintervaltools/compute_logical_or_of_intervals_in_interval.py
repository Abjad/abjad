def compute_logical_or_of_intervals_in_interval(intervals, interval):
    '''Compute the logical OR of a collection of intervals,
    cropped within `interval`.

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return tree

    depth_tree = timeintervaltools.compute_depth_of_intervals_in_interval(tree, interval)
    logic_tree = timeintervaltools.TimeIntervalTree([x for x in depth_tree if 1 <= x['depth']])

    return logic_tree
