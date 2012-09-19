def iterate_staves_forward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    .. note:: Deprecated. Use ``stafftools.iterate_staves_in_expr()`` instead.

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

    return stafftools.iterate_staves_in_expr(
        expr, start=start, stop=stop)
