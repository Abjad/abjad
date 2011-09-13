from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def scale_interval_offsets_by_rational(intervals, rational):
    '''Scale the offset of each interval in `intervals` by
    `rational`, maintaining the lowest offset in `intervals` ::

        abjad> from abjad.tools import intervaltreetools
        abjad> from abjad.tools.intervaltreetools import BoundedInterval
        abjad> from abjad.tools.intervaltreetools import IntervalTree

    ::

        abjad> a = BoundedInterval(-1, 3)
        abjad> b = BoundedInterval(6, 12)
        abjad> c = BoundedInterval(9, 16)
        abjad> tree = IntervalTree([a, b, c])
        abjad> intervaltreetools.scale_interval_offsets_by_rational(tree, Fraction(4, 5))
        IntervalTree([
            BoundedInterval(Offset(-1, 1), Offset(3, 1), {}),
            BoundedInterval(Offset(23, 5), Offset(53, 5), {}),
            BoundedInterval(Offset(7, 1), Offset(14, 1), {})
        ])

    Return interval tree.
    '''

    assert isinstance(rational, (int, Fraction))
    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree or rational == 1:
        return tree

    return IntervalTree([
        x.shift_to_rational(((x.low - tree.low) * rational) + tree.low) \
            for x in tree
    ])
