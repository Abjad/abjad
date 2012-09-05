from abjad.tools import durationtools


def split_intervals_at_rationals(intervals, offsets):
    '''Split `intervals` at each offset in
    `offsets` ::

        >>> from abjad.tools import timeintervaltools
        >>> from abjad.tools.timeintervaltools import TimeInterval
        >>> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        >>> a = TimeInterval(-1, 3)
        >>> b = TimeInterval(6, 12)
        >>> c = TimeInterval(9, 16)
        >>> tree = TimeIntervalTree([a, b, c])
        >>> timeintervaltools.split_intervals_at_rationals(tree, [1, Fraction(19, 2)])
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(1, 1), {}),
            TimeInterval(Offset(1, 1), Offset(3, 1), {}),
            TimeInterval(Offset(6, 1), Offset(19, 2), {}),
            TimeInterval(Offset(9, 1), Offset(19, 2), {}),
            TimeInterval(Offset(19, 2), Offset(12, 1), {}),
            TimeInterval(Offset(19, 2), Offset(16, 1), {})
        ])

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    offsets = [durationtools.Offset(x) for x in offsets]

    if not tree or not offsets:
        return tree

    for offset in offsets:
        intersecting_intervals = set(tree.find_intervals_intersecting_or_tangent_to_offset(offset))
        if not intersecting_intervals:
            continue
        tangent_intervals = tree.find_intervals_starting_or_stopping_at_offset(offset)
        if tangent_intervals:
            intersecting_intervals = intersecting_intervals.difference(set(tangent_intervals))
        splits = []
        for interval in intersecting_intervals:
            splits.extend(interval.split_at_rationals(offset))
        tree = timeintervaltools.TimeIntervalTree(
            set(tree[:]).difference(intersecting_intervals).union(set(splits)))

    return tree
