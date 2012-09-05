from abjad.tools import durationtools


def calculate_depth_centroid_of_intervals_in_interval(intervals, interval):
    '''Return the weighted mean of the depth tree of `intervals` in `interval`,
    such that the centroids of each interval of the depth tree are the values,
    and the weights are the depths at each interval of the depth tree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    depth = timeintervaltools.compute_depth_of_intervals_in_interval(tree, interval)
    weighted_centroids = sum([x.center * x['depth'] for x in depth])
    sum_of_weights = sum([x['depth'] for x in depth])

    if not sum_of_weights:
        return None

    return durationtools.Offset(weighted_centroids) / sum_of_weights
