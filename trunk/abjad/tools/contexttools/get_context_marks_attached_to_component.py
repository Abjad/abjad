from abjad.tools.contexttools.ContextMark import ContextMark


def get_context_marks_attached_to_component(component, klasses=(ContextMark,)):
    r'''.. versionadded:: 2.0

    Get context marks attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})
        abjad> contexttools.DynamicMark('p')(staff[0])
        DynamicMark('p')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            \clef "treble"
            c'8 \p
            d'8
            e'8
            f'8
        }

    ::

        abjad> contexttools.get_context_marks_attached_to_component(staff[0])
        (DynamicMark('p')(c'8),)

    Return tuple of zero or more context marks.

    .. versionchanged:: 2.0
        renamed ``contexttools.get_context_marks_attached_to_component()`` to
        ``contexttools.get_context_marks_attached_to_component()``.
    '''

    result = []
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, klasses):
            result.append(mark)
    return tuple(result)
