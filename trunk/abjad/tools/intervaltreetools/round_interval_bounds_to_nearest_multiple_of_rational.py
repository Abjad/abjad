from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def round_interval_bounds_to_nearest_multiple_of_rational(intervals, rational):
    assert all_are_intervals_or_trees_or_empty(intervals)
    assert isinstance(rational, (int, Fraction)) and 0 < rational

    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree:
        return tree

    intervals = []
    for interval in tree:
        low = Fraction(int(round(interval.low / rational))) * rational
        high = Fraction(int(round(interval.high / rational))) * rational
        if low == high:
            high = low + rational
        intervals.append(interval.shift_to_rational(low).scale_to_rational(high - low))

    return IntervalTree(intervals)
