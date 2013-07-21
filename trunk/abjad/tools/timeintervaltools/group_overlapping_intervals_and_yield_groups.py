def group_overlapping_intervals_and_yield_groups(intervals):
    '''Group overlapping intervals in `intervals`.

    Yield TimeIntervalTrees.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        yield timeintervaltools.TimeIntervalTree([])
        return

    groups = []
    group = [tree[0]]

    # start_offset = group[0].start_offset
    stop_offset = group[0].stop_offset

    for i in range(1, len(tree)):
        if tree[i].start_offset < stop_offset:
            group.append(tree[i])
            if stop_offset < tree[i].stop_offset:
                stop_offset = tree[i].stop_offset
        else:
            groups.append(group)
            group = [tree[i]]
            # start_offset = group[0].start_offset
            stop_offset = group[0].stop_offset

    if group not in groups:
        groups.append(group)

    for group in groups:
        yield timeintervaltools.TimeIntervalTree(group)
