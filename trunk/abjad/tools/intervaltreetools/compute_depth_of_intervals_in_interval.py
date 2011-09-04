from abjad.tools.sequencetools import iterate_sequence_pairwise_strict
from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.intervaltreetools.get_all_unique_bounds_in_intervals import get_all_unique_bounds_in_intervals
from abjad.tools.intervaltreetools.split_intervals_at_rationals import split_intervals_at_rationals


def compute_depth_of_intervals_in_interval(intervals, interval):
    '''Compute a tree whose intervals represent the depth (level of overlap)
    in each boundary pair of `intervals`, cropped within `interval`::

        abjad> from abjad.tools.intervaltreetools import *
        abjad> a = BoundedInterval(0, 3)
        abjad> b = BoundedInterval(6, 12)
        abjad> c = BoundedInterval(9, 15)
        abjad> tree = IntervalTree([a, b, c])
        abjad> d = BoundedInterval(-1, 16)
        abjad> compute_depth_of_intervals_in_interval(tree, d)
        IntervalTree([
            BoundedInterval(Offset(-1, 1), Offset(0, 1), {'depth': 0}),
            BoundedInterval(Offset(0, 1), Offset(3, 1), {'depth': 1}),
            BoundedInterval(Offset(3, 1), Offset(6, 1), {'depth': 0}),
            BoundedInterval(Offset(6, 1), Offset(9, 1), {'depth': 1}),
            BoundedInterval(Offset(9, 1), Offset(12, 1), {'depth': 2}),
            BoundedInterval(Offset(12, 1), Offset(15, 1), {'depth': 1}),
            BoundedInterval(Offset(15, 1), Offset(16, 1), {'depth': 0})
        ])

    Return interval tree.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    assert isinstance(interval, BoundedInterval)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)

    if interval.high <= tree.low or tree.high <= interval.low:
        return IntervalTree([BoundedInterval(interval.low, interval.high, {'depth': 0})])
    else:
        bounds = list(get_all_unique_bounds_in_intervals(tree))
        if interval.low < tree.low:
            bounds.insert(0, interval.low)
        elif tree.low < interval.low:
            bounds = filter(lambda x: interval.low <= x, bounds)
            bounds.insert(0, interval.low)
        if tree.high < interval.high:
            bounds.append(interval.high)
        elif interval.high < tree.high:
            bounds = filter(lambda x: x <= interval.high, bounds)
            bounds.append(interval.high)
        bounds = sorted(list(set(bounds)))

    intervals = []
#   for i in range(len(bounds) - 1):
    for pair in iterate_sequence_pairwise_strict(bounds):
        target = BoundedInterval(pair[0], pair[1], {})
        found = tree.find_intervals_intersecting_or_tangent_to_interval(target)
        if found:
            target['depth'] = len(filter( \
                lambda x: not x.low == target.high and not x.high == target.low, found))
        else:
            target['depth'] = 0
        intervals.append(target)

    return IntervalTree(intervals)
