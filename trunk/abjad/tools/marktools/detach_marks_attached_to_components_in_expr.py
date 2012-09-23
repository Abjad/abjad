def detach_marks_attached_to_components_in_expr(expr):
    r'''.. versionadded:: 2.9

    Detach marks attached to components in `expr`::

        >>> staff = Staff("c'4 \staccato d' \marcato e' \staccato f' \marcato")

    ::

        >>> f(staff)
        \new Staff {
            c'4 -\staccato
            d'4 -\marcato
            e'4 -\staccato
            f'4 -\marcato
        }

    ::

        >>> for mark in marktools.detach_marks_attached_to_components_in_expr(staff):
        ...     mark
        ...
        Articulation('staccato')
        Articulation('marcato')
        Articulation('staccato')
        Articulation('marcato')

    ::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    Return tuple of zero or more detached marks.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import marktools

    result = []
    for component in iterationtools.iterate_components_in_expr(expr):
        result.extend(marktools.detach_marks_attached_to_component(component))

    return tuple(result)
