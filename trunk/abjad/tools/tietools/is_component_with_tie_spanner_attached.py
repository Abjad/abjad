from abjad.tools.componenttools._Component import _Component
from abjad.tools import spannertools
from abjad.tools.tietools.TieSpanner import TieSpanner


def is_component_with_tie_spanner_attached(expr):
    r'''.. versionadded:: 2.0

    True when `expr` is component with tie spanner attached::

        abjad> staff = Staff(notetools.make_repeated_notes(4))
        abjad> tietools.TieSpanner(staff[:])
        TieSpanner(c'8, c'8, c'8, c'8)
        abjad> f(staff)
        \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }
        abjad> tietools.is_component_with_tie_spanner_attached(staff)
        False

    Otherwise false::

        abjad> staff = Staff(notetools.make_repeated_notes(4))
        abjad> tietools.TieSpanner(staff[:])
        TieSpanner(c'8, c'8, c'8, c'8)
        abjad> f(staff)
        \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
        }
        abjad> tietools.is_component_with_tie_spanner_attached(staff[1])
        True

    Return boolean.
    '''

    if not isinstance(expr, _Component):
        return False

    return bool(spannertools.get_spanners_attached_to_component(expr, TieSpanner))
