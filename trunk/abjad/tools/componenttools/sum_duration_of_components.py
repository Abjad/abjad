def sum_duration_of_components(components, preprolated=False, in_seconds=False):
    r'''.. versionadded:: 1.1

    Sum duration of `components`::

        >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
        >>> staff = Staff([tuplet])
        >>> score = Score([staff])
        >>> contexttools.TempoMark(Duration(1, 4), 48)(tuplet[0])
        TempoMark(Duration(1, 4), 48)(c'8)

    ::

        >>> f(score)
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

        >>> show(score) # doctest: +SKIP

    Example 1. Sum duration of components::

        >>> componenttools.sum_duration_of_components(tuplet[:])
        Duration(1, 4)

    Example 2. Sum preprolated duration of components::

        >>> componenttools.sum_duration_of_components(tuplet[:], preprolated=True)
        Duration(3, 8)

    Example 3. Sum duration of components in seconds::

        >>> componenttools.sum_duration_of_components(tuplet[:], in_seconds=True)
        Duration(5, 4)

    Return duration.
    '''

    if in_seconds:
        return sum([component.duration_in_seconds for component in components])
    elif preprolated:
        return sum([component.preprolated_duration for component in components])
    else:
        return sum([component.prolated_duration for component in components])
