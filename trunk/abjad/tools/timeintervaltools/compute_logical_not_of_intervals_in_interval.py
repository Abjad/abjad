def compute_logical_not_of_intervals_in_interval(intervals, interval):
    '''Compute the logical NOT of some collection of intervals,
    cropped within `interval`.

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return tree

    depth_tree = timeintervaltools.compute_depth_of_intervals_in_interval(tree, interval)
    logic_tree = timeintervaltools.TimeIntervalTree([x for x in depth_tree if 0 == x['depth']])

    return logic_tree
