def is_component_with_tempo_mark_attached(expr):
    r'''.. versionadded:: 2.3

    True when `expr` is a component with tempo mark attached::

        >>> score = Score([])
        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)

    ::

        >>> contexttools.TempoMark(Duration(1, 8), 52)(staff)
        TempoMark(Duration(1, 8), 52)(Staff{4})

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                \tempo 8=52
                c'8
                d'8
                e'8
                f'8
            }
        >>

    ::

        >>> contexttools.is_component_with_tempo_mark_attached(staff)
        True

    Otherwise false::

        >>> contexttools.is_component_with_tempo_mark_attached(staff[0])
        False

    Return boolean.
    '''
    from abjad.tools import contexttools

    return contexttools.is_component_with_context_mark_attached(expr, klasses=(contexttools.TempoMark,))
