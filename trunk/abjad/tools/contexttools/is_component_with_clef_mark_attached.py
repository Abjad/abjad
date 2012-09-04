def is_component_with_clef_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component with clef mark attached::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \clef "treble"
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> contexttools.is_component_with_clef_mark_attached(staff)
        True

    False otherwise:

        >>> contexttools.is_component_with_clef_mark_attached(staff[0])
        False

    Return boolean.
    '''
    from abjad.tools import contexttools

    return contexttools.is_component_with_context_mark_attached(expr, (contexttools.ClefMark,))
