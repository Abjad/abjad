from abjad.tools import durationtools


def scale_aggregate_duration_by_rational(intervals, rational):
    '''Scale the aggregate duration of all intervals in `intervals` by
    `rational`, maintaining the original start offset ::

        >>> from abjad.tools import timeintervaltools
        >>> from abjad.tools.timeintervaltools import TimeInterval
        >>> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        >>> a = TimeInterval(-1, 3)
        >>> b = TimeInterval(6, 12)
        >>> c = TimeInterval(9, 16)
        >>> tree = TimeIntervalTree([a, b, c])
        >>> timeintervaltools.scale_aggregate_duration_by_rational(tree, Fraction(1, 3))
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(1, 3), {}),
            TimeInterval(Offset(4, 3), Offset(10, 3), {}),
            TimeInterval(Offset(7, 3), Offset(14, 3), {})
        ])

    Return TimeIntervalTree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    rational = durationtools.Duration(rational)
    assert 0 < rational

    if not tree or rational == 1:
        return tree

    return timeintervaltools.TimeIntervalTree([
        x.shift_to_rational(
            ((x.start - tree.start) * rational) + tree.start).scale_by_rational(rational)\
            for x in tree
    ])
