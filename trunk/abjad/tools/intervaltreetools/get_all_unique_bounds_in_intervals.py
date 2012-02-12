from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def get_all_unique_bounds_in_intervals(intervals):
    '''Return all unique starting and ending boundaries in `intervals`.'''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)

    values = []
    for interval in tree:
        if interval.start not in values:
            values.append(interval.start)
        if interval.stop not in values:
            values.append(interval.stop)
    return tuple(sorted(values))
