def sum_prolated_duration_of_components(components):
    r'''.. versionadded:: 1.1

    Sum prolated duration of `components`::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        >>> f(tuplet)
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        >>> componenttools.sum_prolated_duration_of_components(tuplet[:])
        Duration(1, 4)

    .. versionchanged:: 2.0
        renamed ``durationtools.sum_prolated()`` to
        ``componenttools.sum_prolated_duration_of_components()``.
    '''

    return sum([component.prolated_duration for component in components])
