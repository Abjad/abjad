from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def round_interval_bounds_to_nearest_multiple_of_rational(intervals, rational):
    assert all_are_intervals_or_trees_or_empty(intervals)
    assert isinstance(rational, (int, Fraction)) and 0 < rational

    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree:
        return tree

    intervals = []
    for interval in tree:
        start = Fraction(int(round(interval.start / rational))) * rational
        stop = Fraction(int(round(interval.stop / rational))) * rational
        if start == stop:
            stop = start + rational
        intervals.append(interval.shift_to_rational(start).scale_to_rational(stop - start))

    return TimeIntervalTree(intervals)
