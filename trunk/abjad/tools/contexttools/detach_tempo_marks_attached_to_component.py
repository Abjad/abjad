def detach_tempo_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Detach tempo marks attached to `component`::

        >>> score = Score([])
        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> score.append(staff)

    ::

        >>> tempo_mark = contexttools.TempoMark(Duration(1, 8), 52)
        >>> tempo_mark.attach(staff)
        TempoMark(Duration(1, 8), 52)(Staff{4})

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                \tempo 8=52
                c'4
                d'4
                e'4
                f'4
            }
        >>

    ::

        >>> contexttools.detach_tempo_marks_attached_to_component(staff)
        (TempoMark(Duration(1, 8), 52),)

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
        >>

    Return tuple of zero or more tempo marks.
    '''
    from abjad.tools import contexttools

    marks = []
    for mark in contexttools.get_tempo_marks_attached_to_component(component):
        mark.detach()
        marks.append(mark)

    return tuple(marks)
