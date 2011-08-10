from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def calculate_density_of_attacks_in_interval(intervals, interval):
    '''Return a Fraction of number of attacks in `interval`
    over the magnitude of `interval`.'''

    assert all_are_intervals_or_trees_or_empty(intervals)
    assert isinstance(interval, BoundedInterval)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)

    return len(tree.find_intervals_starting_within_interval(interval)) \
        / interval.magnitude
