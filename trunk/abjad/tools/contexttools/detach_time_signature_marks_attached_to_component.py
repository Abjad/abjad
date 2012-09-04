def detach_time_signature_marks_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach time signature marks attached to `component`::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> contexttools.TimeSignatureMark((4, 4))(staff[0])
        TimeSignatureMark((4, 4))(c'4)

    ::

        >>> f(staff)
        \new Staff {
            \time 4/4
            c'4
            d'4
            e'4
            f'4
        }

    ::

        >>> contexttools.detach_time_signature_marks_attached_to_component(staff[0])
        (TimeSignatureMark((4, 4)),)

    ::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more time signature marks.
    '''
    from abjad.tools import contexttools

    marks = []
    for mark in contexttools.get_time_signature_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)

    return tuple(marks)    
