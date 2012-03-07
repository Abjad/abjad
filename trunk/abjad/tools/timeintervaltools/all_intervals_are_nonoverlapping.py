from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def all_intervals_are_nonoverlapping(intervals):
    '''True when all intervals in `intervals` in tree are non-overlapping.'''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)

    for i in range(1, len(tree)):
        if tree[i].start < tree[i -1].stop:
            return False

    return True
