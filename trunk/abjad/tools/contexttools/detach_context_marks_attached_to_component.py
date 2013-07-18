def detach_context_marks_attached_to_component(component, classes=None):
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

        >>> staff[0].select().detach_marks(contexttools.ContextMark)
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

    if classes is None:
        classes = (contexttools.ContextMark,)

    marks = []
    for mark in component._start_marks[:]:
        if isinstance(mark, classes):
            mark.detach()
            marks.append(mark)
    return tuple(marks)
