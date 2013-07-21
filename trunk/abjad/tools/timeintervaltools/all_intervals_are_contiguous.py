def all_intervals_are_contiguous(intervals):
    '''True when all intervals in `intervals` are contiguous and non-overlapping.
    '''

    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    for i in range(1, len(tree)):
        if tree[i].start_offset != tree[i-1].stop_offset:
            return False

    return True
