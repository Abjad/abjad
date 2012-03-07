from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def scale_aggregate_duration_to_rational(intervals, rational):
    '''Scale the aggregate duration of all intervals in `intervals` to
    `rational`, maintaining the original start offset ::

        abjad> from abjad.tools import timeintervaltools
        abjad> from abjad.tools.timeintervaltools import TimeInterval
        abjad> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        abjad> a = TimeInterval(-1, 3)
        abjad> b = TimeInterval(6, 12)
        abjad> c = TimeInterval(9, 16)
        abjad> tree = TimeIntervalTree([a, b, c])
        abjad> timeintervaltools.scale_aggregate_duration_to_rational(tree, Fraction(16, 7))
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(-55, 119), {}),
            TimeInterval(Offset(-1, 17), Offset(89, 119), {}),
            TimeInterval(Offset(41, 119), Offset(9, 7), {})
        ])

    Return interval tree.
    '''

    assert isinstance(rational, (int, Fraction)) and 0 < rational
    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree or tree.duration == rational:
        return tree

    ratio = rational / tree.duration

    return TimeIntervalTree([
        x.shift_to_rational(
            ((x.start - tree.start) * ratio) + tree.start).scale_by_rational(ratio) \
            for x in tree
    ])
