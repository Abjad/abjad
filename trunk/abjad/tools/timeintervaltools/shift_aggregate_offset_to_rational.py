from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def shift_aggregate_offset_to_rational(intervals, rational):
    '''Shift the aggregate offset of `intervals` to `rational` ::

        abjad> from abjad.tools import timeintervaltools
        abjad> from abjad.tools.timeintervaltools import TimeInterval
        abjad> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        abjad> a = TimeInterval(-1, 3)
        abjad> b = TimeInterval(6, 12)
        abjad> c = TimeInterval(9, 16)
        abjad> tree = TimeIntervalTree([a, b, c])
        abjad> timeintervaltools.shift_aggregate_offset_to_rational(tree, Fraction(10, 7))
        TimeIntervalTree([
            TimeInterval(Offset(10, 7), Offset(38, 7), {}),
            TimeInterval(Offset(59, 7), Offset(101, 7), {}),
            TimeInterval(Offset(80, 7), Offset(129, 7), {})
        ])

    Return interval tree.
    '''

    assert isinstance(rational, (int, Fraction))
    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree or rational == tree.start:
        return tree

    return TimeIntervalTree([
        x.shift_by_rational(rational - tree.start) for x in tree
    ])
