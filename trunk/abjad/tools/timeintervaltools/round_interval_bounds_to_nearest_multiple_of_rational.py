from abjad.tools import durationtools


def round_interval_bounds_to_nearest_multiple_of_rational(intervals, duration):
    '''Round all start and stop offsets of `intervals` to the nearest multiple of `duration`.

    If both start and stop of an interval collapse on the same offset, that interval's stop
    will be adjusted to the next larger multiple of `duration`.

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    duration = durationtools.Duration(duration)
    assert 0 < duration

    if not tree:
        return tree

    intervals = []
    for interval in tree:
        start = durationtools.Offset(int(round(interval.start / duration))) * duration
        stop = durationtools.Offset(int(round(interval.stop / duration))) * duration
        if start == stop:
            stop = start + duration
        intervals.append(interval.shift_to_rational(start).scale_to_rational(stop - start))

    return timeintervaltools.TimeIntervalTree(intervals)
