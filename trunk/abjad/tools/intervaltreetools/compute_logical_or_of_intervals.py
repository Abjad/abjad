from abjad.tools.intervaltreetools.BoundedInterval import BoundedInterval
from abjad.tools.intervaltreetools.IntervalTree import IntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.intervaltreetools.compute_depth_of_intervals import compute_depth_of_intervals
from abjad.tools.intervaltreetools.fuse_tangent_or_overlapping_intervals import fuse_tangent_or_overlapping_intervals


def compute_logical_or_of_intervals(intervals):
    '''Compute the logical OR of a collection of intervals.'''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, IntervalTree):
        tree = intervals
    else:
        tree = IntervalTree(intervals)
    if not tree:
        return tree

    depth_tree = compute_depth_of_intervals(tree)
    #logic_tree = IntervalTree(filter(lambda x: 1 <= x['depth'], depth_tree))
    logic_tree = IntervalTree([x for x in depth_tree if 1 <= x['depth']])

    return logic_tree

#   if not logic_tree:
#      return logic_tree
#   return fuse_tangent_or_overlapping_intervals(logic_tree)
