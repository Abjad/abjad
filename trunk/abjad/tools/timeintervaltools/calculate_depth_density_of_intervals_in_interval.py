from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.timeintervaltools.compute_depth_of_intervals_in_interval import compute_depth_of_intervals_in_interval
from abjad.tools.timeintervaltools.split_intervals_at_rationals import split_intervals_at_rationals
from abjad import Fraction


def calculate_depth_density_of_intervals_in_interval(intervals, interval):
    '''Return a Fraction, of the duration of each interval in the
    depth tree of `intervals` within `interval`, multiplied by the depth at that interval,
    divided by the overall duration of `intervals`.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    assert isinstance(interval, TimeInterval)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)

    split_tree = split_intervals_at_rationals(tree, [interval.start, interval.stop])
    split_tree = TimeIntervalTree(split_tree.find_intervals_starting_and_stopping_within_interval(interval))

    if not split_tree:
        return Fraction(0)
    return Fraction(sum([x.duration for x in split_tree])) / interval.duration

#   depth = compute_depth_of_intervals_in_interval(tree, interval)
#   return Fraction(sum([x.duration * x['depth'] for x in depth])) \
#      / depth.duration
