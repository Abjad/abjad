from abjad.tools import durationtools


def calculate_sustain_centroid_of_intervals(intervals):
    '''Return a weighted mean, such that the centroid of each interval
    in `intervals` are the values, and the weights are their durations.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return None

    weighted_centroids = sum([(x.center * x.duration) for x in tree])
    sum_of_weights = sum([x.duration for x in tree])
    return durationtools.Offset(weighted_centroids) / sum_of_weights
