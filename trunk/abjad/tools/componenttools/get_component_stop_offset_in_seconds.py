def get_component_stop_offset_in_seconds(component):
    r'''.. versionadded:: 1.1

    Get `component` stop offset in seconds::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> score = Score([staff])
        >>> contexttools.TempoMark(Duration(1, 4), 52)(score)
        TempoMark(Duration(1, 4), 52)(Score<<1>>)
        >>> f(score) # doctest: +SKIP
        \new Score <<
            \new Staff {
                \tempo 4=52
                c'8
                d'8
                e'8
                f'8
            }
        >>

    ::

        >>> componenttools.get_component_stop_offset_in_seconds(score.leaves[1])
        Offset(15, 13)

    Return positive fraction.
    '''

    return component.stop_offset_in_seconds
