from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def group_overlapping_intervals_and_yield_groups(intervals):
    '''Group overlapping intervals in `intervals` and
        return tuples.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree:
        yield TimeIntervalTree([])
        return

    groups = []
    group = [tree[0]]

    # start = group[0].start
    stop = group[0].stop

    for i in range(1, len(tree)):
        if tree[i].start < stop:
            group.append(tree[i])
            if stop < tree[i].stop:
                stop = tree[i].stop
        else:
            groups.append(group)
            group = [tree[i]]
            # start = group[0].start
            stop = group[0].stop

    if group not in groups:
        groups.append(group)

    for group in groups:
        yield tuple(group)
