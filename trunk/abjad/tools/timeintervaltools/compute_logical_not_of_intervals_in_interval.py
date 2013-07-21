def compute_logical_not_of_intervals_in_interval(
    intervals, bounding_interval):
    '''Compute the logical NOT of some collection of intervals,
    cropped within `interval`.

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    return timeintervaltools.compute_logical_not_of_intervals(
        intervals, bounding_interval=bounding_interval)

