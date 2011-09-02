from abjad.tools.contexttools.DynamicMark import DynamicMark
from abjad.tools.contexttools.get_context_marks_attached_to_component import get_context_marks_attached_to_component


def get_dynamic_marks_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get dynamic marks attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.DynamicMark('p')(staff[0])
        DynamicMark('p')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 \p
            d'8
            e'8
            f'8
        }

    ::

        abjad> contexttools.get_dynamic_marks_attached_to_component(staff[0])
        (DynamicMark('p')(c'8),)

    Return tuple of zero or more dynamic marks.
    '''

    return get_context_marks_attached_to_component(component, klasses=(DynamicMark,))
