from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def clip_interval_durations_to_range(intervals, min = None, max = None):
    assert all_are_intervals_or_trees_or_empty(intervals)
    assert all([isinstance(x, (int, Fraction, type(None))) for x in [min, max]])
    if isinstance(min, (int, Fraction)):
        assert 0 < min
    if isinstance(max, (int, Fraction)):
        assert 0 < max
    if isinstance(min, (int, Fraction)) and isinstance(max, (int, Fraction)):
        assert min <= max

    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree:
        return tree

    intervals = []
    for interval in tree:
        if min is not None and interval.duration < min:
            intervals.append(interval.scale_to_rational(min))
        elif max is not None and max < interval.duration:
            intervals.append(interval.scale_to_rational(max))
        else:
            intervals.append(interval)

    return IntervalTree(intervals)
