def compute_logical_and_of_intervals_in_interval(
    intervals, bounding_interval):
    '''Compute the logical AND of a collection of intervals,
    cropped within `interval`.

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    return timeintervaltools.compute_logical_and_of_intervals(
        intervals, bounding_interval)
