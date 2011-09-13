# TODO: implement leaftools.fuse_leaves_little_endian()
def fuse_leaves_big_endian(leaves):
    r'''.. versionadded:: 1.1

    Fuse thread-contiguous `leaves`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> leaftools.fuse_leaves_big_endian(staff[1:])
        [Note("d'4.")]
        abjad> f(staff)
        \new Staff {
            c'8
            d'4.
        }

    Rewrite duration of first leaf in `leaves`.

    Detach all leaves in `leaves` other than first leaf from score.

    Return list of first leaf in `leaves`.

    .. versionchanged:: 2.0
        renamed ``fuse.leaves_by_reference()`` to
        ``leaftools.fuse_leaves_big_endian()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import leaftools

    assert componenttools.all_are_thread_contiguous_components(leaves)

    if len(leaves) <= 1:
        return leaves

    total_preprolated = componenttools.sum_preprolated_duration_of_components(leaves)
    componenttools.remove_component_subtree_from_score_and_spanners(leaves[1:])
    return leaftools.set_preprolated_leaf_duration(leaves[0], total_preprolated)
