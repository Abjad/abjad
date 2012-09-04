def get_time_signature_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get time signature marks attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.TimeSignatureMark((2, 4))(staff)
        TimeSignatureMark((2, 4))(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \time 2/4
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> contexttools.get_time_signature_marks_attached_to_component(staff)
        (TimeSignatureMark((2, 4))(Staff{4}),)

    Return tuple of zero or more time_signature marks.
    '''
    from abjad.tools import contexttools

    return contexttools.get_context_marks_attached_to_component(
        component, klasses=(contexttools.TimeSignatureMark,))
