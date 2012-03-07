from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def scale_aggregate_duration_by_rational(intervals, rational):
    '''Scale the aggregate duration of all intervals in `intervals` by
    `rational`, maintaining the original start offset ::

        abjad> from abjad.tools import timeintervaltools
        abjad> from abjad.tools.timeintervaltools import TimeInterval
        abjad> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        abjad> a = TimeInterval(-1, 3)
        abjad> b = TimeInterval(6, 12)
        abjad> c = TimeInterval(9, 16)
        abjad> tree = TimeIntervalTree([a, b, c])
        abjad> timeintervaltools.scale_aggregate_duration_by_rational(tree, Fraction(1, 3))
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(1, 3), {}),
            TimeInterval(Offset(4, 3), Offset(10, 3), {}),
            TimeInterval(Offset(7, 3), Offset(14, 3), {})
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
        x.shift_to_rational(
            ((x.start - tree.start) * rational) + tree.start).scale_by_rational(rational)\
            for x in tree
    ])
