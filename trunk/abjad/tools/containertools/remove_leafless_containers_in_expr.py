from abjad.tools import componenttools


def remove_leafless_containers_in_expr(expr):
    r'''Remove empty containers in `expr`::

        >>> staff = Staff("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 } { b'8 c''8 }")
        >>> beamtools.BeamSpanner(staff[:])
        BeamSpanner({c'8, d'8}, {e'8, f'8}, {g'8, a'8}, {b'8, c''8})

    ::

        >>> containertools.delete_contents_of_container(staff[1])
        [Note("e'8"), Note("f'8")]
        >>> containertools.delete_contents_of_container(staff[-1])
        [Note("b'8"), Note("c''8")]

    ::

        >>> f(staff)
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

        >>> containertools.remove_leafless_containers_in_expr(staff)

    ::

        >>> f(staff)
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
        ``containertools.remove_leafless_containers_in_expr()``.
    '''
    from abjad.tools import iterationtools

    for container in iterationtools.iterate_containers_in_expr(expr):
        if not container.leaves:
            componenttools.remove_component_subtree_from_score_and_spanners([container])
