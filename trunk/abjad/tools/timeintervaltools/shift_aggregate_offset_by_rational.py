from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def shift_aggregate_offset_by_rational(intervals, rational):
    '''Shift the aggregate offset of `intervals` by `rational` ::

        abjad> from abjad.tools import timeintervaltools
        abjad> from abjad.tools.timeintervaltools import TimeInterval
        abjad> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        abjad> a = TimeInterval(-1, 3)
        abjad> b = TimeInterval(6, 12)
        abjad> c = TimeInterval(9, 16)
        abjad> tree = TimeIntervalTree([a, b, c])
        abjad> timeintervaltools.shift_aggregate_offset_by_rational(tree, Fraction(1, 3))
        TimeIntervalTree([
            TimeInterval(Offset(-2, 3), Offset(10, 3), {}),
            TimeInterval(Offset(19, 3), Offset(37, 3), {}),
            TimeInterval(Offset(28, 3), Offset(49, 3), {})
        ])

    Return interval tree.
    '''

    assert isinstance(rational, (int, Fraction))
    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree or rational == 0:
        return tree

    return TimeIntervalTree([
        x.shift_by_rational(rational) for x in tree
    ])
