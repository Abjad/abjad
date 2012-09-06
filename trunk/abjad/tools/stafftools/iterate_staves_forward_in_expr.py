from abjad.tools import componenttools


def iterate_staves_forward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    Iterate staves forward in `expr`::

        >>> score = Score(4 * Staff([]))

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
            }
            \new Staff {
            }
            \new Staff {
            }
            \new Staff {
            }
        >>

    ::

        >>> for staff in stafftools.iterate_staves_forward_in_expr(score):
        ...     staff
        ...
        Staff{}
        Staff{}
        Staff{}
        Staff{}

    Return generator.
    '''
    from abjad.tools import stafftools

    return componenttools.iterate_components_forward_in_expr(
        expr, stafftools.Staff, start=start, stop=stop)
