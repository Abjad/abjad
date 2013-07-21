def compute_logical_not_of_intervals(intervals, bounding_interval=None):
    '''Compute the logical NOT of some collection of intervals.

    Return TimeIntervalTree.
    '''

    from abjad.tools import timeintervaltools

    depth_tree = timeintervaltools.compute_depth_of_intervals(
        intervals, bounding_interval=bounding_interval)
    logic_tree = timeintervaltools.TimeIntervalTree([
        x for x in depth_tree if 0 == x['depth']])

    return logic_tree
