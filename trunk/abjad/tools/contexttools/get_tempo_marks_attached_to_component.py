def get_tempo_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get tempo marks attached to `component`::

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

        >>> contexttools.get_tempo_marks_attached_to_component(staff)
        (TempoMark(Duration(1, 8), 52)(Staff{4}),)

    Return tuple of zero or more tempo marks.
    '''
    from abjad.tools import contexttools

    return contexttools.get_context_marks_attached_to_component(component, klasses=(contexttools.TempoMark,))
