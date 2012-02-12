from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def scale_interval_durations_to_rational(intervals, rational):
    '''Scale the duration of each interval in `intervals` to
    `rational`, maintaining their start offsets ::

        abjad> from abjad.tools import intervaltreetools
        abjad> from abjad.tools.intervaltreetools import BoundedInterval
        abjad> from abjad.tools.intervaltreetools import IntervalTree

    ::

        abjad> a = BoundedInterval(-1, 3)
        abjad> b = BoundedInterval(6, 12)
        abjad> c = BoundedInterval(9, 16)
        abjad> tree = IntervalTree([a, b, c])
        abjad> intervaltreetools.scale_interval_durations_to_rational(tree, Fraction(1, 7))
        IntervalTree([
            BoundedInterval(Offset(-1, 1), Offset(-6, 7), {}),
            BoundedInterval(Offset(6, 1), Offset(43, 7), {}),
            BoundedInterval(Offset(9, 1), Offset(64, 7), {})
        ])

    Return interval tree.
    '''

    assert isinstance(rational, (int, Fraction)) and 0 < rational
    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree:
        return tree

    return IntervalTree([
        x.scale_to_rational(rational) for x in tree
    ])
