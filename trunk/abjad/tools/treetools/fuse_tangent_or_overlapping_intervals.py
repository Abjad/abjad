from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.all_are_intervals_or_trees_or_empty \
    import all_are_intervals_or_trees_or_empty
from abjad.tools.treetools.group_tangent_or_overlapping_intervals_and_yield_groups import \
    group_tangent_or_overlapping_intervals_and_yield_groups 

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

    assert all_are_intervals_or_trees_or_empty(intervals)
    tree = IntervalTree(intervals)
    if not tree:
        return tree

    trees = [IntervalTree(group) for group in \
        group_tangent_or_overlapping_intervals_and_yield_groups(tree)]

    return IntervalTree([
        BoundedInterval(tree.low_min, tree.high_max) for tree in trees
    ])

