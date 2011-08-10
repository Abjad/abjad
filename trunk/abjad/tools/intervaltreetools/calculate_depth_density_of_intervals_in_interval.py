from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.intervaltreetools.compute_depth_of_intervals_in_interval import compute_depth_of_intervals_in_interval
from abjad.tools.intervaltreetools.split_intervals_at_rationals import split_intervals_at_rationals
from abjad import Fraction


def calculate_depth_density_of_intervals_in_interval(intervals, interval):
    '''Return a Fraction, of the magnitude of each interval in the
    depth tree of `intervals` within `interval`, multiplied by the depth at that interval,
    divided by the overall magnitude of `intervals`.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    assert isinstance(interval, BoundedInterval)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)

    split_tree = split_intervals_at_rationals(tree, [interval.low, interval.high])
    split_tree = IntervalTree(split_tree.find_intervals_starting_and_stopping_within_interval(interval))

    if not split_tree:
        return Fraction(0)
    return Fraction(sum([x.magnitude for x in split_tree])) / interval.magnitude

#   depth = compute_depth_of_intervals_in_interval(tree, interval)
#   return Fraction(sum([x.magnitude * x['depth'] for x in depth])) \
#      / depth.magnitude
