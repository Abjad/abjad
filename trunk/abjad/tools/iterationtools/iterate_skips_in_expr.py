from abjad.tools import skiptools


def iterate_skips_in_expr(expr, reverse=False, start=0, stop=None):
    r'''.. versionadded:: 2.10


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

        >>> for skip in iterationtools.iterate_skips_in_expr(staff):
        ...   skip
        Skip('s8')
        Skip('s2')

    Iterate skips backwards in `expr`:

    ::

        >>> for skip in iterationtools.iterate_skips_in_expr(staff, reverse=True):
        ...   skip
        Skip('s2')
        Skip('s8')

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import iterationtools

    return iterationtools.iterate_components_in_expr(
        expr, klass=skiptools.Skip, reverse=reverse, start=start, stop=stop)
