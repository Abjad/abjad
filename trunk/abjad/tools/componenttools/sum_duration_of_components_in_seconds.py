def sum_duration_of_components_in_seconds(components):
    r'''.. versionadded:: 1.1

    Sum duration of `components` in seconds::

        abjad> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        abjad> score = Score([Staff([tuplet])])
        abjad> contexttools.TempoMark(Duration(1, 4), 48)(score)
        TempoMark(4, 48)(Score<<1>>)
        abjad> f(score) # doctest: +SKIP
        \new Score <<
            \new Staff {
                \times 2/3 {
                    \tempo 4=48
                    c'8
                    d'8
                    e'8
                }
            }
        >>

    ::

        abjad> componenttools.sum_duration_of_components_in_seconds(tuplet[:])
        Duration(5, 4)

    .. versionchanged:: 2.0
        renamed ``durationtools.sum_seconds()`` to
        ``componenttools.sum_duration_of_components_in_seconds()``.
    '''

    assert isinstance(components, list)
    return sum([component.duration_in_seconds for component in components])
