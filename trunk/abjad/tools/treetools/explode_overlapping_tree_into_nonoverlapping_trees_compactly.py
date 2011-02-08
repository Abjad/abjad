from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools import compute_depth_of_tree


def explode_overlapping_tree_into_nonoverlapping_trees_compactly(tree):
    '''Explode the intervals in `tree` into n non-overlapping trees, 
    where n is the maximum depth of `tree`.

    Returns an array of `IntervalTree` instances.

    The algorithm will attempt to insert the exploded intervals
    into the lowest-indexed resultant tree with free space.
    '''
    
    assert isinstance(tree, IntervalTree)

    depth_tree = compute_depth_of_tree(tree)
    max_depth = max([x.data['depth'] for x in depth_tree])
    xtrees = [IntervalTree([ ]) for i in range(max_depth)]

    for interval in tree.inorder:
        for xtree in xtrees:
            if not len(xtree):
                xtree.insert(interval)
                break
            elif not xtree.inorder[-1].is_overlapped_by_interval(interval):
                xtree.insert(interval)
                break
                
    return xtrees
