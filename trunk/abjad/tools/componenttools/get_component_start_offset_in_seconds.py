def get_component_start_offset_in_seconds(component):
    r'''.. versionadded:: 1.1

    Get `component` start offset in seconds::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> score = Score([staff])
        abjad> contexttools.TempoMark(Duration(1, 4), 52)(score)
        TempoMark(Duration(1, 4), 52)(Score<<1>>)
        abjad> f(score) # doctest: +SKIP
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

        abjad> componenttools.get_component_start_offset_in_seconds(score.leaves[1])
        Offset(15, 26)

    Return nonnegative fraction.
    '''

    return component._offset.start_in_seconds
