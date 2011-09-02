from abjad.tools.contexttools.ClefMark import ClefMark
from abjad.tools.contexttools.get_context_marks_attached_to_component import get_context_marks_attached_to_component


def get_clef_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get clef marks attached to `component`::

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

        abjad> contexttools.get_clef_marks_attached_to_component(staff)
        (ClefMark('treble')(Staff{4}),)

    Return tuple of zero or more clef marks.
    '''

    return get_context_marks_attached_to_component(component, klasses=(ClefMark,))
