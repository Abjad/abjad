def detach_context_marks_attached_to_component(component, klasses=None):
    r'''.. versionadded:: 2.0

    Detach context marks attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef_mark = contexttools.ClefMark('treble')(staff)
        >>> dynamic_mark = contexttools.DynamicMark('p')(staff[0])
        >>> f(staff)
        \new Staff {
            \clef "treble"
            c'8 \p
            d'8
            e'8
            f'8
        }

    ::

        >>> contexttools.detach_context_marks_attached_to_component(staff[0])
        (DynamicMark('p'),)

    ::

        >>> f(staff)
        \new Staff {
            \clef "treble"
            c'8
            d'8
            e'8
            f'8
        }

    Return tuple of zero or context marks.
    '''
    from abjad.tools import contexttools

    if klasses is None:
        klasses = (contexttools.ContextMark,)

    marks = []
    for mark in component._marks_for_which_component_functions_as_start_component[:]:
        if isinstance(mark, klasses):
            mark.detach()
            marks.append(mark)
    return tuple(marks)
