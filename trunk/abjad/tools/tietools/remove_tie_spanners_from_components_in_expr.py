from abjad.tools import spannertools


def remove_tie_spanners_from_components_in_expr(expr):
    r'''Remove tie spanners components in `expr`::

        >>> staff = Staff("c'4 ~ c'16 d'4 ~ d'16")

    ::

        >>> f(staff)
        \new Staff {
            c'4 ~
            c'16
            d'4 ~
            d'16
        }

    ::

        >>> tietools.remove_tie_spanners_from_components_in_expr(staff[:])
        [Note("c'4"), Note("c'16"), Note("d'4"), Note("d'16")]

    ::

        >>> f(staff)
        \new Staff {
            c'4
            c'16
            d'4
            d'16
        }

    Return `expr`.

    .. versionchanged:: 2.0
        renamed ``componenttools.untie_shallow()`` to
        ``tietools.remove_tie_spanners_from_components_in_expr()``.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import tietools

    for component in iterationtools.iterate_components_in_expr(expr):
        spannertools.destroy_spanners_attached_to_component(component, tietools.TieSpanner)

    return expr
