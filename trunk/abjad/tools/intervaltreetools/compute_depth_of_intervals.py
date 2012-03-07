from abjad.tools.intervaltreetools.TimeInterval import TimeInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.intervaltreetools.get_all_unique_bounds_in_intervals import get_all_unique_bounds_in_intervals
from abjad.tools.intervaltreetools.split_intervals_at_rationals import split_intervals_at_rationals


def compute_depth_of_intervals(intervals):
    '''Compute a tree whose intervals represent the depth (level of overlap)
    in each boundary pair of `intervals`::

        abjad> from abjad.tools.intervaltreetools import *
        abjad> a = TimeInterval(0, 3)
        abjad> b = TimeInterval(6, 12)
        abjad> c = TimeInterval(9, 15)
        abjad> tree = IntervalTree([a, b, c])
        abjad> compute_depth_of_intervals(tree)
        IntervalTree([
            TimeInterval(Offset(0, 1), Offset(3, 1), {'depth': 1}),
            TimeInterval(Offset(3, 1), Offset(6, 1), {'depth': 0}),
            TimeInterval(Offset(6, 1), Offset(9, 1), {'depth': 1}),
            TimeInterval(Offset(9, 1), Offset(12, 1), {'depth': 2}),
            TimeInterval(Offset(12, 1), Offset(15, 1), {'depth': 1})
        ])

    Return interval tree.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)

    bounds = list(get_all_unique_bounds_in_intervals(tree))
    intervals = []
    for i in range(len(bounds) - 1):
        target = TimeInterval(bounds[i], bounds[i+1], {})
        found = tree.find_intervals_intersecting_or_tangent_to_interval(target)
        if found:
            # depth = len(filter(lambda x: (not x.start == target.stop and not x.stop == target.start), found))
            depth = len([x for x in found \
                if (not x.start == target.stop and not x.stop == target.start)])
        else:
            depth = 0
        target['depth'] = depth
        intervals.append(target)

    return IntervalTree(intervals)
