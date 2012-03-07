from abjad.tools.durationtools import Offset
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def calculate_mean_release_of_intervals(intervals):
    '''Return a Fraction of the average release offset of `intervals`.'''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree:
        return None
    return Offset(sum([i.stop for i in tree])) / len(tree)
