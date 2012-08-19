def sum_preprolated_duration_of_components(components):
    r'''.. versionadded:: 1.1

    Sum preprolated duration of `components`::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        >>> componenttools.sum_preprolated_duration_of_components(tuplet[:])
        Duration(3, 8)

    Return zero on empty iterable::

        >>> componenttools.sum_preprolated_duration_of_components([])
        0

    Raise contiguity error on nonparent-contiguous `components`::

        >>> t = Voice(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")

    ::

        >>> f(t)
        \new Voice {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                f'8
                g'8
                a'8
            }
        }
        >>> componenttools.sum_preprolated_duration_of_components(t.leaves)
        Duration(3, 4)

    .. versionchanged:: 2.0
        renamed ``componenttools.get_duration_preprolated()`` to
        ``componenttools.sum_preprolated_duration_of_components()``.
    '''

    # sum preprolated durations
    result = sum([component.preprolated_duration for component in components])

    # return sum
    return result
