from abjad.tools.durationtools import Offset
from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.intervaltreetools.compute_depth_of_intervals_in_interval import compute_depth_of_intervals_in_interval


def calculate_depth_centroid_of_intervals_in_interval(intervals, interval):
    '''Return the weighted mean of the depth tree of `intervals` in `interval`,
    such that the centroids of each interval of the depth tree are the values,
    and the weights are the depths at each interval of the depth tree.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    assert isinstance(interval, BoundedInterval)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    depth = compute_depth_of_intervals_in_interval(tree, interval)
    weighted_centroids = sum([x.centroid * x['depth'] for x in depth])
    sum_of_weights = sum([x['depth'] for x in depth])
    if not sum_of_weights:
        return None
    return Offset(weighted_centroids) / sum_of_weights
