from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.group_all_contiguous_or_overlapping_intervals_in_tree_and_yield_groups import \
    group_all_contiguous_or_overlapping_intervals_in_tree_and_yield_groups 

def fuse_tangent_or_overlapping_intervals(intervals):
    '''Fuse all tangent or overlapping intervals and return an `IntervalTree`
    of the result ::

        abjad> tree = IntervalTree([ ])
        abjad> tree.insert(BoundedInterval(0, 10))
        abjad> tree.insert(BoundedInterval(5, 15))
        abjad> tree.insert(BoundedInterval(15, 25))
        abjad> fuse_tangent_or_overlapping_intervals(tree)
        IntervalTree([
            BoundedInterval(0, 25, data = {}),
        ])
    '''

    assert len(intervals)    
    assert all([isinstance(interval, BoundedInterval) \
        for interval in intervals])

    trees = [IntervalTree(group) for group in \
        group_all_contiguous_or_overlapping_intervals_in_tree_and_yield_groups(intervals)]

    return IntervalTree([
        BoundedInterval(tree.low_min, tree.high_max) for tree in trees
    ])

