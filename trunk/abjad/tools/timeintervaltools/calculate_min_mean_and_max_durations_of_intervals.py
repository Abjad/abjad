from abjad.tools import durationtools


def calculate_min_mean_and_max_durations_of_intervals(intervals):
    '''Return a 3-tuple of the minimum, mean and maximum duration of all intervals in `intervals`.
    If `intervals` is empty, return None.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return None

    durations = [x.duration for x in tree]
    return (min(durations), durationtools.Duration(sum(durations), len(durations)), max(durations))
