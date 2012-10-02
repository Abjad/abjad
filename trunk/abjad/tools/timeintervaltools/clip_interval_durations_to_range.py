from abjad.tools import durationtools


def clip_interval_durations_to_range(intervals, minimum=None, maximum=None):
    from abjad.tools import timeintervaltools

    assert timeintervaltools.all_are_intervals_or_trees_or_empty(intervals)

    if minimum is not None:
        minimum = durationtools.Duration(minimum)
        assert 0 < minimum

    if maximum is not None:
        maximum = durationtools.Duration(maximum)
        assert 0 < maximum

    if minimum is not None and maximum is not None:
        assert minimum < maximum

    if isinstance(intervals, timeintervaltools.TimeIntervalTree):
        tree = intervals
    else:
        tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return tree

    intervals = []
    for interval in tree:
        if minimum is not None and interval.duration < minimum:
            intervals.append(interval.scale_to_rational(minimum))
        elif maximum is not None and maximum < interval.duration:
            intervals.append(interval.scale_to_rational(maximum))
        else:
            intervals.append(interval)

    return timeintervaltools.TimeIntervalTree(intervals)
