# TODO: change name to remove_leafless_containers_in_expr()
# TODO: add remove_empty_containers_in_expr() that operates on pure emptiness rather than leaflessness
def remove_empty_containers_in_expr(expr):
    r'''Remove empty containers in `expr`::

        abjad> staff = Staff(Container(notetools.make_repeated_notes(2)) * 4)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff.leaves)
        abjad> beamtools.BeamSpanner(staff[:])
        BeamSpanner({c'8, d'8}, {e'8, f'8}, {g'8, a'8}, {b'8, c''8})
        abjad> containertools.delete_contents_of_container(staff[1])
        [Note("e'8"), Note("f'8")]
        abjad> containertools.delete_contents_of_container(staff[-1])
        [Note("b'8"), Note("c''8")]

    ::

        abjad> f(staff)
        \new Staff {
            {
                c'8 [
                d'8
            }
            {
            }
            {
                g'8
                a'8 ]
            }
            {
            }
        }

    ::

        abjad> containertools.remove_empty_containers_in_expr(staff)

    ::

        abjad> f(staff)
        \new Staff {
            {
                c'8 [
                d'8
            }
            {
                g'8
                a'8 ]
            }
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``containertools.remove_empty()`` to
        ``containertools.remove_empty_containers_in_expr()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import containertools

    for container in containertools.iterate_containers_forward_in_expr(expr):
        if not container.leaves:
            componenttools.remove_component_subtree_from_score_and_spanners([container])
