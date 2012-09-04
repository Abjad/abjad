def get_effective_dynamic(component):
    r'''.. versionadded:: 2.0

    Get effective dynamic of `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.DynamicMark('f')(staff[0])
        DynamicMark('f')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 \f
            d'8
            e'8
            f'8
        }

    ::

        >>> for note in staff:
        ...     print note, contexttools.get_effective_dynamic(note)
        ...
        c'8 DynamicMark('f')(c'8)
        d'8 DynamicMark('f')(c'8)
        e'8 DynamicMark('f')(c'8)
        f'8 DynamicMark('f')(c'8)

    Return dynamic mark or none.
    '''
    from abjad.tools import contexttools

    return contexttools.get_effective_context_mark(component, contexttools.DynamicMark)
