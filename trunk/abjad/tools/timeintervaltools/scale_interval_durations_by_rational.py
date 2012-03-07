from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def scale_interval_durations_by_rational(intervals, rational):
    '''Scale the duration of each interval in `intervals` by
    `rational`, maintaining their start offsets ::

        abjad> from abjad.tools import timeintervaltools
        abjad> from abjad.tools.timeintervaltools import TimeInterval
        abjad> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        abjad> a = TimeInterval(-1, 3)
        abjad> b = TimeInterval(6, 12)
        abjad> c = TimeInterval(9, 16)
        abjad> tree = TimeIntervalTree([a, b, c])
        abjad> timeintervaltools.scale_interval_durations_by_rational(tree, Fraction(6, 5))
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(19, 5), {}),
            TimeInterval(Offset(6, 1), Offset(66, 5), {}),
            TimeInterval(Offset(9, 1), Offset(87, 5), {})
        ])

    Return interval tree.
    '''

    assert isinstance(rational, (int, Fraction)) and 0 < rational
    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree or rational == 1:
        return tree

    return TimeIntervalTree([
        x.scale_by_rational(rational) for x in tree
    ])
