from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools import compute_depth_of_intervals


def explode_tree_uncompactly(tree):
    '''Explode the intervals in `tree` into n non-overlapping trees, 
    where n is the maximum depth of `tree`.

    Returns an array of `IntervalTree` instances.

    The algorithm will attempt to insert the exploded intervals
    cyclically, making its insertion attempt at the next resultant tree
    in the array, rather than always beginning its search from index 0.
    '''

    assert isinstance(tree, IntervalTree)

    depth_tree = compute_depth_of_intervals(tree)
    max_depth = max([x.data['depth'] for x in depth_tree])
    layers = [[ ] for i in range(max_depth)]

    offset = 0
    for interval in tree.inorder:
        for i in range(max_depth):
            layer = layers[(i + offset) % max_depth]
            if not len(layer):
                layer.append(interval)
                offset = i + 1
                break
            elif not layer[-1].is_overlapped_by_interval(interval):
                layer.append(interval)
                offset = i + 1
                break

    return [IntervalTree(layer) for layer in layers]
