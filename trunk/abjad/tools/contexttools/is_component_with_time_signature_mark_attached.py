def is_component_with_time_signature_mark_attached(expr):
    r'''.. versionadded:: 2.0

    True when `expr` is a component with time signature mark attached::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.TimeSignatureMark((4, 8))(staff[0])
        TimeSignatureMark((4, 8))(c'8)

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

        >>> contexttools.is_component_with_time_signature_mark_attached(staff[0])
        True

    Otherwise false::

        >>> contexttools.is_component_with_time_signature_mark_attached(staff)
        False

    Return boolean.
    '''
    from abjad.tools import contexttools

    return contexttools.is_component_with_context_mark_attached(expr, (contexttools.TimeSignatureMark,))
