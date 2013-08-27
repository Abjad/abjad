# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import selectiontools
Selection = selectiontools.Selection


def fuse_leaves(leaves):
    r'''Fuse logical-voice-contiguous `leaves`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> leaftools.fuse_leaves(staff[1:])
        [Note("d'4.")]

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8
            d'4.
        }

    Rewrite duration of first leaf in `leaves`.

    Detach all leaves in `leaves` other than first leaf from score.

    Return selection of first leaf in `leaves`.
    '''
    from abjad.tools import leaftools
    from abjad.tools import selectiontools

    assert Selection._all_are_contiguous_components_in_same_logical_voice(
        leaves)
    if not isinstance(leaves, selectiontools.SliceSelection):
        leaves = selectiontools.SliceSelection(leaves)

    if len(leaves) <= 1:
        return leaves

    total_preprolated = leaves._preprolated_duration
    for leaf in leaves[1:]:
        parent = leaf._parent
        if parent:
            index = parent.index(leaf)
            del(parent[index])
            
    return leaftools.set_leaf_duration(leaves[0], total_preprolated)
