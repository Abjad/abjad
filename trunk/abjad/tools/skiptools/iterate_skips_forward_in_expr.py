def iterate_skips_forward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    .. note:: Deprecated. Use ``skiptools.iterate_skips_in_expr()`` instead.

    Iterate skips forward in `expr`::

        >>> staff = Staff("<e' g' c''>8 a'8 s8 <d' f' b'>8 s2")

    ::

        >>> f(staff)
        \new Staff {
            <e' g' c''>8
            a'8
            s8
            <d' f' b'>8
            s2
        }

    ::

        >>> for skip in skiptools.iterate_skips_forward_in_expr(staff):
        ...   skip
        Skip('s8')
        Skip('s2')

    Ignore threads.

    Return generator.
    '''

    from abjad.tools import skiptools

    return skiptools.iterate_skips_in_expr(expr, start=start, stop=stop)
