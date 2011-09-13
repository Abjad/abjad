from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools.spannertools import Spanner
from abjad.tools.spannertools.iterate_components_backward_in_spanner import iterate_components_backward_in_spanner
from abjad.tools.spannertools.iterate_components_forward_in_spanner import iterate_components_forward_in_spanner


def get_nth_leaf_in_spanner(spanner, idx):
    '''Get nth leaf in spanner, no matter how complicated the nesting
    situation.


    .. versionchanged:: 2.0
        renamed ``spannertools.get_nth_leaf()`` to
        ``spannertools.get_nth_leaf_in_spanner()``.
    '''

    if not isinstance(idx, (int, long)):
        raise TypeError

    if 0 <= idx:
        leaves = iterate_components_forward_in_spanner(spanner, klass = _Leaf)
        for leaf_index, leaf in enumerate(leaves):
            if leaf_index == idx:
                return leaf
    else:
        leaves = iterate_components_backward_in_spanner(spanner, klass = _Leaf)
        for leaf_index, leaf in enumerate(leaves):
            leaf_number = -leaf_index - 1
            if leaf_number == idx:
                return leaf

    raise IndexError
