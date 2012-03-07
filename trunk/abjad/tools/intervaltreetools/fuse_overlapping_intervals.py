from abjad.tools.intervaltreetools.TimeInterval import TimeInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.intervaltreetools.group_overlapping_intervals_and_yield_groups import group_overlapping_intervals_and_yield_groups

def fuse_overlapping_intervals(intervals):
    '''Fuse the overlapping intervals in `intervals` and return an `IntervalTree`
    of the result ::

        abjad> from abjad.tools import intervaltreetools
        abjad> from abjad.tools.intervaltreetools import TimeInterval
        abjad> from abjad.tools.intervaltreetools import IntervalTree

    ::

        abjad> a = TimeInterval(0, 10)
        abjad> b = TimeInterval(5, 15)
        abjad> c = TimeInterval(15, 25)
        abjad> tree = IntervalTree([a, b, c])
        abjad> intervaltreetools.fuse_overlapping_intervals(tree)
        IntervalTree([
            TimeInterval(Offset(0, 1), Offset(15, 1), {}),
            TimeInterval(Offset(15, 1), Offset(25, 1), {})
        ])

    Return interval tree.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree:
        return tree

    trees = [IntervalTree(group) for group in \
        group_overlapping_intervals_and_yield_groups(tree)]

    return IntervalTree([
        TimeInterval(tree.earliest_start, tree.latest_stop) for tree in trees
    ])
