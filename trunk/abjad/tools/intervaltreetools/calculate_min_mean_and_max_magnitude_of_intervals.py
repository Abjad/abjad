from abjad.tools.durationtools import Duration
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty


def calculate_min_mean_and_max_magnitude_of_intervals(intervals):
    '''Return a 3-tuple of the minimum, mean and maximum magnitude of all intervals in `intervals`.
    If `intervals` is empty, return None.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree:
        return None

    magnitudes = [x.magnitude for x in tree]
    return (min(magnitudes), Duration(sum(magnitudes), len(magnitudes)), max(magnitudes))
