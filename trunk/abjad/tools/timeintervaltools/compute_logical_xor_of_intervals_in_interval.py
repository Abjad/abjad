def compute_logical_xor_of_intervals_in_interval(
    intervals, bounding_interval):
    '''Compute the logical XOR of a collections of intervals,
    cropped within `interval`.

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    depth_tree = timeintervaltools.compute_depth_of_intervals(
        intervals, bounding_interval=bounding_interval)
    logic_tree = timeintervaltools.TimeIntervalTree([
        x for x in depth_tree if 1 == x['depth']])

    return logic_tree
