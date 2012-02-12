from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def scale_aggregate_duration_to_rational(intervals, rational):
    '''Scale the aggregate duration of all intervals in `intervals` to
    `rational`, maintaining the original start offset ::

        abjad> from abjad.tools import intervaltreetools
        abjad> from abjad.tools.intervaltreetools import BoundedInterval
        abjad> from abjad.tools.intervaltreetools import IntervalTree

    ::

        abjad> a = BoundedInterval(-1, 3)
        abjad> b = BoundedInterval(6, 12)
        abjad> c = BoundedInterval(9, 16)
        abjad> tree = IntervalTree([a, b, c])
        abjad> intervaltreetools.scale_aggregate_duration_to_rational(tree, Fraction(16, 7))
        IntervalTree([
            BoundedInterval(Offset(-1, 1), Offset(-55, 119), {}),
            BoundedInterval(Offset(-1, 17), Offset(89, 119), {}),
            BoundedInterval(Offset(41, 119), Offset(9, 7), {})
        ])

    Return interval tree.
    '''

    assert isinstance(rational, (int, Fraction)) and 0 < rational
    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree or tree.duration == rational:
        return tree

    ratio = rational / tree.duration

    return IntervalTree([
        x.shift_to_rational(
            ((x.start - tree.start) * ratio) + tree.start).scale_by_rational(ratio) \
            for x in tree
    ])
