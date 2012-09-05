from abjad.tools import durationtools


def scale_interval_offsets_by_rational(intervals, rational):
    '''Scale the starting offset of each interval in `intervals` by
    `rational`, maintaining the startest offset in `intervals` ::

        >>> from abjad.tools import timeintervaltools
        >>> from abjad.tools.timeintervaltools import TimeInterval
        >>> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        >>> a = TimeInterval(-1, 3)
        >>> b = TimeInterval(6, 12)
        >>> c = TimeInterval(9, 16)
        >>> tree = TimeIntervalTree([a, b, c])
        >>> timeintervaltools.scale_interval_offsets_by_rational(tree, Fraction(4, 5))
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(3, 1), {}),
            TimeInterval(Offset(23, 5), Offset(53, 5), {}),
            TimeInterval(Offset(7, 1), Offset(14, 1), {})
        ])

    Return interval tree.
    '''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    rational = durationtools.Duration(rational)

    if not tree or rational == 1:
        return tree

    return timeintervaltools.TimeIntervalTree([
        x.shift_to_rational(((x.start - tree.start) * rational) + tree.start) \
            for x in tree
    ])
