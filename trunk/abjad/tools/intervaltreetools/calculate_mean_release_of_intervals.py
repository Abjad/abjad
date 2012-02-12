from abjad.tools.durationtools import Offset
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def calculate_mean_release_of_intervals(intervals):
    '''Return a Fraction of the average release offset of `intervals`.'''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree:
        return None
    return Offset(sum([i.stop for i in tree])) / len(tree)
