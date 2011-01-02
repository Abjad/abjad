from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools import compute_depth_of_tree


def explode_overlapping_tree_into_nonoverlapping_trees_uncompactly(tree):
    '''Explode the intervals in `tree` into n non-overlapping trees, 
    where n is the maximum depth of `tree`.

    Returns an array of `IntervalTree`s.

    The algorithm will attempt to insert the exploded intervals
    cyclically, making its insertion attempt at the next resultant tree
    in the array, rather than always beginning its search from index 0.
    '''

    assert isinstance(tree, IntervalTree)

    depth_tree = compute_depth_of_tree(tree)
    max_depth = max([x.data['depth'] for x in depth_tree])
    xtrees = [IntervalTree([ ]) for i in range(max_depth)]

    offset = 0
    for interval in tree.inorder:
        for i in range(max_depth):
            xtree = xtrees[(i + offset) % max_depth]
            if not len(xtree):
                xtree.insert(interval)
                offset = i + 1
                break
            elif not xtree.inorder[-1].is_overlapped_by_interval(interval):
                xtree.insert(interval)
                offset = i + 1
                break

    return xtrees
