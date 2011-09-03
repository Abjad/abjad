from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def group_tangent_or_overlapping_intervals_and_yield_groups(intervals):
    '''Group tangent or overlapping intervals in `intervals` and
        return tuples.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree:
        yield IntervalTree([])
        return

    groups = []
    group = [tree[0]]

    low = group[0].low
    high = group[0].high

    for i in range(1, len(tree)):
        if tree[i].low <= high:
            group.append(tree[i])
            if high < tree[i].high:
                high = tree[i].high
        else:
            groups.append(group)
            group = [tree[i]]
            low = group[0].low
            high = group[0].high

    if group not in groups:
        groups.append(group)

    for x in groups:
        yield tuple(x)
