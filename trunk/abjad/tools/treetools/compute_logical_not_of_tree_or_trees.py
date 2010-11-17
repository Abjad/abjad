from abjad.tools.treetools.BoundedInterval import BoundedInterval
from abjad.tools.treetools.IntervalTree import IntervalTree
from abjad.tools.treetools.compute_depth_of_tree import compute_depth_of_tree


def compute_logical_not_of_tree_or_trees(trees):
    '''Compute the logical NOT of the intervals in a tree or group of trees.'''

    if isinstance(trees, IntervalTree):
        merge_tree = trees   
    elif isinstance(trees, (list, set, tuple)):
        assert len(trees)
        assert all([isinstance(tree, IntervalTree) for tree in trees])
        merge_tree = IntervalTree( )
        for tree in trees:
            merge_tree.insert(tree)
    else:
        raise ValueError

    if not merge_tree:
        return IntervalTree( )

    depth_tree = compute_depth_of_tree(merge_tree)
    logic_tree = IntervalTree(filter(lambda x: 0 == x.data['depth'], depth_tree))

    groups = [ ]
    group = [logic_tree.inorder[0]]
    for i in range(1, len(logic_tree)):
        if logic_tree.inorder[i].low == logic_tree.inorder[i - 1].high:
            group.append(logic_tree.inorder[i])
        else:
            groups.append(group)
            group = [logic_tree.inorder[i]]

    if group not in groups:
        groups.append(group)

    output_tree = IntervalTree( )
    for group in groups:
        low = group[0].low
        high = group[-1].high
        output_tree.insert(BoundedInterval(low, high))

    return output_tree
