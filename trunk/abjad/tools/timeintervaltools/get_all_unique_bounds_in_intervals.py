def get_all_unique_bounds_in_intervals(intervals):
    '''Find all unique starting and ending boundaries in `intervals`.

    Return list of Offsets.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    values = []
    for interval in tree:
        if interval.start not in values:
            values.append(interval.start)
        if interval.stop not in values:
            values.append(interval.stop)
    return tuple(sorted(values))
