from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.timeintervaltools.compute_depth_of_intervals import compute_depth_of_intervals
from abjad import Fraction


def calculate_depth_density_of_intervals(intervals):
    '''Return a Fraction, of the duration of each interval in the
    depth tree of `intervals`, multiplied by the depth at that interval,
    divided by the overall duration of `intervals`.

    The depth density of a single interval is 1 ::

        abjad> from abjad.tools import timeintervaltools
        abjad> from abjad.tools.timeintervaltools import TimeInterval
        abjad> from abjad.tools.timeintervaltools import TimeIntervalTree

    ::

        abjad> a = TimeInterval(0, 1)
        abjad> b = TimeInterval(0, 1)
        abjad> c = TimeInterval(Fraction(1, 2), 1)
        abjad> timeintervaltools.calculate_depth_density_of_intervals(a)
        Duration(1, 1)
        abjad> timeintervaltools.calculate_depth_density_of_intervals([a, b])
        Duration(2, 1)
        abjad> timeintervaltools.calculate_depth_density_of_intervals([a, c])
        Duration(3, 2)
        abjad> timeintervaltools.calculate_depth_density_of_intervals([a, b, c])
        Duration(5, 2)

    Return fraction.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)

    if not tree:
        return Fraction(0)
    return Fraction(sum([x.duration for x in tree])) / tree.duration

#   depth = compute_depth_of_intervals(tree)
#   return Fraction(sum([x.duration * x['depth'] for x in depth])) \
#      / depth.duration
