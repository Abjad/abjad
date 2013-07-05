from abjad.tools import leaftools


def get_nth_leaf_in_spanner(spanner, n):
    '''Get leaf `n` in spanner.
    
    Complexity of score tree nesting doesn't matter.  

    Return leaf.
    '''
    from abjad.tools import spannertools

    if not isinstance(n, (int, long)):
        raise TypeError

    component_classes = (leaftools.Leaf, )

    if 0 <= n:
        leaves = spannertools.iterate_components_in_spanner(
            spanner, component_classes=component_classes)
        for leaf_index, leaf in enumerate(leaves):
            if leaf_index == n:
                return leaf
    else:
        leaves = spannertools.iterate_components_in_spanner(
            spanner, component_classes=component_classes, reverse=True)
        for leaf_index, leaf in enumerate(leaves):
            leaf_number = -leaf_index - 1
            if leaf_number == n:
                return leaf

    raise IndexError
