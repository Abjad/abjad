def iterate_rests_backward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    .. note:: Deprecated. Use ``resttools.iterate_rests_in_expr()`` instead.

    Iterate rests backward in `expr`::

        >>> staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

    ::

        >>> f(staff)
        \new Staff {
            <e' g' c''>8
            a'8
            r8
            <d' f' b'>8
            r2
        }

    ::

        >>> for rest in resttools.iterate_rests_backward_in_expr(staff):
        ...   rest
        Rest('r2')
        Rest('r8')

    Ignore threads.

    Return generator.
    '''

    from abjad.tools import resttools

    return resttools.iterate_rests_in_expr(expr, reverse=True, start=start, stop=stop)
