def detach_dynamic_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Detach dynamic marks attached to `component`::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> dynamic_mark = contexttools.DynamicMark('p')
        >>> dynamic_mark.attach(staff[0])
        DynamicMark('p')(c'4)

    ::

        >>> f(staff)
        \new Staff {
            c'4 \p
            d'4
            e'4
            f'4
        }

    ::

        >>> contexttools.detach_dynamic_marks_attached_to_component(staff[0])
        (DynamicMark('p'),)

    ::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more dynamic marks.
    '''
    from abjad.tools import contexttools

    marks = []
    for mark in contexttools.get_dynamic_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)

    return tuple(marks)
