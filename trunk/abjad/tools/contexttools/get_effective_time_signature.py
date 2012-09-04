def get_effective_time_signature(component):
    r'''.. versionadded:: 2.0

    Get effective time signature of `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.TimeSignatureMark((4, 8))(staff)
        TimeSignatureMark((4, 8))(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> for note in staff:
        ...     note, contexttools.get_effective_time_signature(note)
        ...
        (Note("c'8"), TimeSignatureMark((4, 8))(Staff{4}))
        (Note("d'8"), TimeSignatureMark((4, 8))(Staff{4}))
        (Note("e'8"), TimeSignatureMark((4, 8))(Staff{4}))
        (Note("f'8"), TimeSignatureMark((4, 8))(Staff{4}))

    Return time signature mark or none.
    '''
    from abjad.tools import contexttools

    return contexttools.get_effective_context_mark(component, contexttools.TimeSignatureMark)
