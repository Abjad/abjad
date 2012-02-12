from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def all_intervals_are_nonoverlapping(intervals):
    '''True when all intervals in `intervals` in tree are non-overlapping.'''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)

    for i in range(1, len(tree)):
        if tree[i].start < tree[i -1].stop:
            return False

    return True
