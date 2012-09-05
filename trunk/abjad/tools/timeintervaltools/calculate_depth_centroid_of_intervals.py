from abjad.tools import durationtools


def calculate_depth_centroid_of_intervals(intervals):
    '''Calculate the weighted mean offset of `intervals`, such that the
    centroids of each interval in the depth tree of `intervals` make up
    the values of the mean, and the depth of each interval in the depth
    tree of `intervals` make up the weights.

    Return Offset.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return None

    depth = timeintervaltools.compute_depth_of_intervals(tree)
    weighted_centroids = sum([x.center * x['depth'] for x in depth])
    sum_of_weights = sum([x['depth'] for x in depth])
    if not sum_of_weights:
        return None
    return durationtools.Offset(weighted_centroids) / sum_of_weights
