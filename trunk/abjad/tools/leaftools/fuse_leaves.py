from abjad.tools import componenttools


def fuse_leaves(leaves):
    r'''.. versionadded:: 1.1

    Fuse thread-contiguous `leaves`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> leaftools.fuse_leaves(staff[1:])
        [Note("d'4.")]
        >>> f(staff)
        \new Staff {
            c'8
            d'4.
        }

    Rewrite duration of first leaf in `leaves`.

    Detach all leaves in `leaves` other than first leaf from score.

    Return list of first leaf in `leaves`.
    '''
    from abjad.tools import leaftools

    assert componenttools.all_are_thread_contiguous_components(leaves)

    if len(leaves) <= 1:
        return leaves

    total_preprolated = componenttools.sum_duration_of_components(leaves, preprolated=True)
    componenttools.remove_component_subtree_from_score_and_spanners(leaves[1:])
    return leaftools.set_preprolated_leaf_duration(leaves[0], total_preprolated)
