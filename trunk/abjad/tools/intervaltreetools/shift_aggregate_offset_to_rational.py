from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def shift_aggregate_offset_to_rational(intervals, rational):
    '''Shift the aggregate offset of `intervals` to `rational` ::

        abjad> from abjad.tools import intervaltreetools
        abjad> from abjad.tools.intervaltreetools import BoundedInterval
        abjad> from abjad.tools.intervaltreetools import IntervalTree

    ::

        abjad> a = BoundedInterval(-1, 3)
        abjad> b = BoundedInterval(6, 12)
        abjad> c = BoundedInterval(9, 16)
        abjad> tree = IntervalTree([a, b, c])
        abjad> intervaltreetools.shift_aggregate_offset_to_rational(tree, Fraction(10, 7))
        IntervalTree([
            BoundedInterval(Offset(10, 7), Offset(38, 7), {}),
            BoundedInterval(Offset(59, 7), Offset(101, 7), {}),
            BoundedInterval(Offset(80, 7), Offset(129, 7), {})
        ])

    Return interval tree.
    '''

    assert isinstance(rational, (int, Fraction))
    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree or rational == tree.start:
        return tree

    return IntervalTree([
        x.shift_by_rational(rational - tree.start) for x in tree
    ])
