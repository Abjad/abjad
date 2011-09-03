from abjad.tools.contexttools.ClefMark import ClefMark
from abjad.tools.contexttools.is_component_with_context_mark_attached import is_component_with_context_mark_attached


def is_component_with_clef_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component with clef mark attached::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \clef "treble"
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> contexttools.is_component_with_clef_mark_attached(staff)
        True

    False otherwise:

        abjad> contexttools.is_component_with_clef_mark_attached(staff[0])
        False

    Return boolean.
    '''

    return is_component_with_context_mark_attached(expr, (ClefMark,))
