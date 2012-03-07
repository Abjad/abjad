from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad import Fraction


def calculate_density_of_attacks_in_interval(intervals, interval):
    '''Return a Fraction of number of attacks in `interval`
    over the duration of `interval`.'''

    assert all_are_intervals_or_trees_or_empty(intervals)
    assert isinstance(interval, TimeInterval)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)

    return len(tree.find_intervals_starting_within_interval(interval)) \
        / interval.duration
