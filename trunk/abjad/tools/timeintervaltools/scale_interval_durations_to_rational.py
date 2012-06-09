from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from fractions import Fraction


def scale_interval_durations_to_rational(intervals, rational):
    '''Scale the duration of each interval in `intervals` to
    `rational`, maintaining their start offsets ::

        >>> from abjad.tools import timeintervaltools
        >>> from abjad.tools.timeintervaltools import TimeInterval
        >>> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        >>> a = TimeInterval(-1, 3)
        >>> b = TimeInterval(6, 12)
        >>> c = TimeInterval(9, 16)
        >>> tree = TimeIntervalTree([a, b, c])
        >>> timeintervaltools.scale_interval_durations_to_rational(tree, Fraction(1, 7))
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(-6, 7), {}),
            TimeInterval(Offset(6, 1), Offset(43, 7), {}),
            TimeInterval(Offset(9, 1), Offset(64, 7), {})
        ])

    Return interval tree.
    '''

    assert isinstance(rational, (int, Fraction)) and 0 < rational
    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree:
        return tree

    return TimeIntervalTree([
        x.scale_to_rational(rational) for x in tree
    ])
