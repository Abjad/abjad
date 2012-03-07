from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def split_intervals_at_rationals(intervals, rationals):
    '''Split `intervals` at each rational in
    `rationals` ::

        abjad> from abjad.tools import timeintervaltools
        abjad> from abjad.tools.timeintervaltools import TimeInterval
        abjad> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        abjad> a = TimeInterval(-1, 3)
        abjad> b = TimeInterval(6, 12)
        abjad> c = TimeInterval(9, 16)
        abjad> tree = TimeIntervalTree([a, b, c])
        abjad> timeintervaltools.split_intervals_at_rationals(tree, [1, Fraction(19, 2)])
        TimeIntervalTree([
            TimeInterval(Offset(-1, 1), Offset(1, 1), {}),
            TimeInterval(Offset(1, 1), Offset(3, 1), {}),
            TimeInterval(Offset(6, 1), Offset(19, 2), {}),
            TimeInterval(Offset(9, 1), Offset(19, 2), {}),
            TimeInterval(Offset(19, 2), Offset(12, 1), {}),
            TimeInterval(Offset(19, 2), Offset(16, 1), {})
        ])

    Return interval tree.
    '''

    assert len(rationals)
    assert all([isinstance(x, (int, Fraction)) for x in rationals])
    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree or not rationals:
        return tree

    for rational in rationals:
        intersecting_intervals = set(tree.find_intervals_intersecting_or_tangent_to_offset(rational))
        if not intersecting_intervals:
            continue
        tangent_intervals = tree.find_intervals_starting_or_stopping_at_offset(rational)
        if tangent_intervals:
            intersecting_intervals = intersecting_intervals.difference(set(tangent_intervals))
        splits = []
        for interval in intersecting_intervals:
            splits.extend(interval.split_at_rationals(rational))
        tree = TimeIntervalTree(set(tree[:]).difference(intersecting_intervals).union(set(splits)))

    return tree
