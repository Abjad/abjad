def get_effective_tempo(component):
    r'''.. versionadded:: 2.0

    Get effective tempo of `component`::

        >>> score = Score([])
        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> contexttools.TempoMark(Duration(1, 8), 52)(staff[0])
        TempoMark(Duration(1, 8), 52)(c'8)

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

        >>> for note in staff:
        ...     print note, contexttools.get_effective_tempo(note)
        ...
        c'8 TempoMark(Duration(1, 8), 52)(c'8)
        d'8 TempoMark(Duration(1, 8), 52)(c'8)
        e'8 TempoMark(Duration(1, 8), 52)(c'8)
        f'8 TempoMark(Duration(1, 8), 52)(c'8)

    Return tempo mark or none.
    '''
    from abjad.tools import contexttools

    return contexttools.get_effective_context_mark(component, contexttools.TempoMark)
