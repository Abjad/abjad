from abjad.tools.timeintervaltools.TimeInterval import TimeInterval
from abjad.tools.timeintervaltools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.timeintervaltools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.timeintervaltools.compute_depth_of_intervals import compute_depth_of_intervals
from abjad.tools.timeintervaltools.fuse_tangent_or_overlapping_intervals import fuse_tangent_or_overlapping_intervals


def compute_logical_xor_of_intervals(intervals):
    '''Compute the logical XOR of a collections of intervals.'''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree:
        return tree

    depth_tree = compute_depth_of_intervals(tree)
    #logic_tree = TimeIntervalTree(filter(lambda x: 1 == x['depth'], depth_tree))
    logic_tree = TimeIntervalTree([x for x in depth_tree if 1 == x['depth']])

    return logic_tree
