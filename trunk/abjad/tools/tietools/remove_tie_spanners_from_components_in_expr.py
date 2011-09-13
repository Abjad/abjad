from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner


def remove_tie_spanners_from_components_in_expr(expr):
    r'''Remove tie spanners components in `expr`::

        abjad> staff = Staff("c'4 ~ c'16 d'4 ~ d'16")
        abjad> f(staff)
        \new Staff {
            c'4 ~
            c'16
            d'4 ~
            d'16
        }

    ::

        abjad> tietools.remove_tie_spanners_from_components_in_expr(staff[:])
        [Note("c'4"), Note("c'16"), Note("d'4"), Note("d'16")]
        abjad> f(staff)
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
    from abjad.tools import componenttools

    for component in componenttools.iterate_components_forward_in_expr(expr):
        spannertools.destroy_all_spanners_attached_to_component(component, TieSpanner)

    return expr
