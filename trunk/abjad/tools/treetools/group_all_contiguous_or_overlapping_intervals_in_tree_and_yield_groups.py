from abjad.tools.treetools.IntervalTree import IntervalTree


def group_all_contiguous_or_overlapping_intervals_in_tree_and_yield_groups(tree):
    assert isinstance(tree, IntervalTree)

    if not tree:
        yield IntervalTree( )
        return
    
    groups = [ ]
    group = [tree.inorder[0]]

    low = group[0].low
    high = group[0].high

    for i in range(1, len(tree.inorder)):
        if tree.inorder[i].low <= high:
            group.append(tree.inorder[i])
            if high < tree.inorder[i].high:
                high = tree.inorder[i].high
        else:
            groups.append(group)
            group = [tree.inorder[i]]
            low = group[0].low
            high = group[0].high

    if group not in groups:
        groups.append(group)

    for x in groups:               
        yield tuple(x)

