def fuse_tangent_or_overlapping_intervals(intervals):
    '''Fuse all tangent or overlapping intervals and return an `TimeIntervalTree` of the result ::

        >>> from abjad.tools import timeintervaltools
        >>> from abjad.tools.timeintervaltools import TimeInterval
        >>> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        >>> a = TimeInterval(0, 10)
        >>> b = TimeInterval(5, 15)
        >>> c = TimeInterval(15, 25)
        >>> tree = TimeIntervalTree([a, b, c])
        >>> timeintervaltools.fuse_tangent_or_overlapping_intervals(tree)
        TimeIntervalTree([
            TimeInterval(Offset(0, 1), Offset(25, 1), {})
        ])

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return tree

    trees = [timeintervaltools.TimeIntervalTree(group) for group in \
        timeintervaltools.group_tangent_or_overlapping_intervals_and_yield_groups(tree)]

    return timeintervaltools.TimeIntervalTree([
        timeintervaltools.TimeInterval(tree.earliest_start, tree.latest_stop) for tree in trees
    ])
