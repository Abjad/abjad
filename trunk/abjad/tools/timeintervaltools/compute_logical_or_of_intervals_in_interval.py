def compute_logical_or_of_intervals_in_interval(
    intervals, bounding_interval):
    '''Compute the logical OR of a collection of intervals,
    cropped within `interval`.

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    return timeintervaltools.compute_logical_or_of_intervals(
        intervals, bounding_interval=bounding_interval)
