from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
   import all_are_intervals_or_trees_or_empty
from abjad.tools.treetools.compute_depth_of_intervals import compute_depth_of_intervals
from abjad.tools.treetools.fuse_tangent_or_overlapping_intervals \
    import fuse_tangent_or_overlapping_intervals


def compute_logical_and_of_intervals(intervals):
    '''Compute the logical AND of a collection of intervals.'''

    assert all_are_intervals_or_trees_or_empty(intervals)
    tree = IntervalTree(intervals)
    if not tree:
        return tree

    depth_tree = compute_depth_of_intervals(tree)
    logic_tree = IntervalTree(filter(lambda x: 1 < x.data['depth'], depth_tree))

    if not logic_tree:
        return logic_tree
    return fuse_tangent_or_overlapping_intervals(logic_tree)
