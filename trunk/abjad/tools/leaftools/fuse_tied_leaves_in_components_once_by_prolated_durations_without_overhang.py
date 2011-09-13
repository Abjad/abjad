def fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang(
    components, prolated_durations):
    r'''.. versionadded:: 1.1

    Fuse tied leaves in `components` once by `prolated_durations` without overhang::

        abjad> staff = Staff(notetools.make_repeated_notes(8))
        abjad> tietools.TieSpanner(staff.leaves)
        TieSpanner(c'8, c'8, c'8, c'8, c'8, c'8, c'8, c'8)
        abjad> f(staff)
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

        abjad> leaftools.fuse_tied_leaves_in_components_once_by_prolated_durations_without_overhang(staff, [Duration(3, 8), Duration(3, 8)])

    ::

        abjad> f(staff)
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
    from abjad.tools import componenttools
    from abjad.tools import leaftools
    from abjad.tools import tietools

    # get duration groups
    groups = \
        componenttools.partition_components_once_by_prolated_durations_exactly_without_overhang(
        components, prolated_durations)

    for group in groups:
        # get tie_chains intersecting this group
        tie_chains = tietools.get_tie_chains_in_expr(group)

        for chain in tie_chains:
            leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(chain)
