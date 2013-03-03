from abjad.tools import leaftools


def get_nth_leaf_in_spanner(spanner, idx):
    '''Get nth leaf in spanner, no matter how complicated the nesting
    situation.

    Return leaf.
    '''
    from abjad.tools import spannertools

    if not isinstance(idx, (int, long)):
        raise TypeError

    if 0 <= idx:
        leaves = spannertools.iterate_components_in_spanner(spanner, klass=leaftools.Leaf)
        for leaf_index, leaf in enumerate(leaves):
            if leaf_index == idx:
                return leaf
    else:
        leaves = spannertools.iterate_components_in_spanner(spanner, klass=leaftools.Leaf, reverse=True)
        for leaf_index, leaf in enumerate(leaves):
            leaf_number = -leaf_index - 1
            if leaf_number == idx:
                return leaf

    raise IndexError
