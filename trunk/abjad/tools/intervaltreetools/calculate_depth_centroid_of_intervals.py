from abjad.tools.durationtools import Offset
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.intervaltreetools.compute_depth_of_intervals import compute_depth_of_intervals


def calculate_depth_centroid_of_intervals(intervals):
    '''Return a weighted mean, such that the centroids of each interval
    in the depth tree of `intervals` are the values,
    and the depth of each interval in the depth tree of `intervals`
    are the weights.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree:
        return None
    depth = compute_depth_of_intervals(tree)
    weighted_centroids = sum([x.centroid * x['depth'] for x in depth])
    sum_of_weights = sum([x['depth'] for x in depth])
    if not sum_of_weights:
        return None
    return Offset(weighted_centroids) / sum_of_weights
