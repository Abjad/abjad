from abjad.tools import durationtools


def scale_aggregate_duration_to_rational(intervals, rational):
    '''Scale the aggregate duration of all intervals in `intervals` to
    `rational`, maintaining the original start offset ::

        >>> from abjad.tools import timeintervaltools
        >>> from abjad.tools.timeintervaltools import TimeInterval
        >>> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        >>> a = TimeInterval(-1, 3)
        >>> b = TimeInterval(6, 12)
        >>> c = TimeInterval(9, 16)
        >>> tree = TimeIntervalTree([a, b, c])
        >>> timeintervaltools.scale_aggregate_duration_to_rational(tree, Fraction(16, 7))
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(-55, 119), {}),
            TimeInterval(Offset(-1, 17), Offset(89, 119), {}),
            TimeInterval(Offset(41, 119), Offset(9, 7), {})
        ])

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    rational = durationtools.Duration(rational)
    assert 0 < rational

    if not tree or tree.duration == rational:
        return tree

    ratio = rational / tree.duration

    return timeintervaltools.TimeIntervalTree([
        x.shift_to_rational(
            ((x.start - tree.start) * ratio) + tree.start).scale_by_rational(ratio) \
            for x in tree
    ])
