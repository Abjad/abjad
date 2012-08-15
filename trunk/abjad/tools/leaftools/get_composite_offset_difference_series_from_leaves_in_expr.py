from abjad.tools import mathtools


def get_composite_offset_difference_series_from_leaves_in_expr(expr):
    r'''.. versionadded:: 2.0

    Get composite offset difference series from leaves in `expr`::

        >>> staff_1 = Staff(r"\times 4/3 { c'8 d'8 e'8 }")
        >>> staff_2 = Staff("f'8 g'8 a'8 b'8")
        >>> score = Score([staff_1, staff_2])

    ::

        >>> f(score)
            \new Score <<
                \new Staff {
                    \fraction \times 4/3 {
                        c'8
                        d'8
                        e'8
                    }
                }
                \new Staff {
                    f'8
                    g'8
                    a'8
                    b'8
                }
            >>

    ::

        >>> for x in leaftools.get_composite_offset_difference_series_from_leaves_in_expr(score):
        ...     x
        ...
        Duration(1, 8)
        Duration(1, 24)
        Duration(1, 12)
        Duration(1, 12)
        Duration(1, 24)
        Duration(1, 8)

    Composite offset difference series defined equal to time intervals between
    unique start and stop offsets of leaves in `expr`.

    Return list of durations.
    '''
    from abjad.tools import leaftools

    composite_offset_series = leaftools.get_composite_offset_series_from_leaves_in_expr(expr)

    return list(mathtools.difference_series(composite_offset_series))
