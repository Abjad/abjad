from abjad.tools.tietools.TieSpanner import TieSpanner


def is_component_with_tie_spanner_attached(expr):
    r'''.. versionadded:: 2.0

    True when `expr` is component with tie spanner attached::

        abjad> staff = Staff("c'8 ~ c' ~ c' ~ c'")

    ::

        abjad> f(staff)
        \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }

    ::

        abjad> tietools.is_component_with_tie_spanner_attached(staff[1])
        True

    Otherwise false::

        abjad> tietools.is_component_with_tie_spanner_attached(staff)
        False

    Return boolean.
    '''
    from abjad.tools import componenttools
    from abjad.tools import spannertools

    if not isinstance(expr, componenttools.Component):
        return False

    return bool(spannertools.get_spanners_attached_to_component(expr, TieSpanner))
