from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.timeintervaltools.group_overlapping_intervals_and_yield_groups import group_overlapping_intervals_and_yield_groups

def fuse_overlapping_intervals(intervals):
    '''Fuse the overlapping intervals in `intervals` and return an `TimeIntervalTree`
    of the result ::

        abjad> from abjad.tools import timeintervaltools
        abjad> from abjad.tools.timeintervaltools import TimeInterval
        abjad> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        abjad> a = TimeInterval(0, 10)
        abjad> b = TimeInterval(5, 15)
        abjad> c = TimeInterval(15, 25)
        abjad> tree = TimeIntervalTree([a, b, c])
        abjad> timeintervaltools.fuse_overlapping_intervals(tree)
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(15, 1), {}),
            TimeInterval(Offset(15, 1), Offset(25, 1), {})
        ])

    Return interval tree.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree:
        return tree

    trees = [TimeIntervalTree(group) for group in \
        group_overlapping_intervals_and_yield_groups(tree)]

    return TimeIntervalTree([
        TimeInterval(tree.earliest_start, tree.latest_stop) for tree in trees
    ])
