from abjad.tools.treetools.IntervalTree import IntervalTree


def all_intervals_in_tree_are_contiguous(tree):
    assert isinstance(tree, IntervalTree)
    
    for i in range(1, len(tree.intervals)):
        if tree.inorder[i].low != tree.inorder[i-1].high:
            return False

    return True
