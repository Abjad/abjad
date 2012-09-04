from abjad.tools import componenttools


def fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang(
    components, prolated_durations):
    r'''.. versionadded:: 1.1

    Fuse tied leaves in `components` once by `prolated_durations` without overhang::

        >>> staff = Staff(notetools.make_repeated_notes(8))
        >>> tietools.TieSpanner(staff.leaves)
        TieSpanner(c'8, c'8, c'8, c'8, c'8, c'8, c'8, c'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8 ~
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }

    ::

        >>> leaftools.fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang(
        ... staff, [Duration(3, 8), Duration(3, 8)])

    ::

        >>> f(staff)
        \new Staff {
            c'4. ~
            c'4. ~
            c'8 ~
            c'8
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``fuse.tied_leaves_by_prolated_durations()`` to
        ``leaftools.fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang()``.
    '''
    from abjad.tools import leaftools
    from abjad.tools import tietools

    # get duration groups
    groups = \
        componenttools.partition_components_by_durations_exactly(
        components, prolated_durations, cyclic=False, in_seconds=False, overhang=False)

    for group in groups:
        # get tie chains intersecting this group
        tie_chains = tietools.get_nontrivial_tie_chains_masked_by_components(group)

        for tie_chain in tie_chains:
            leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(tie_chain)
