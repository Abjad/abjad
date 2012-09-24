from abjad.tools import resttools


def iterate_rests_in_expr(expr, reverse=False, start=0, stop=None):
    r'''.. versionadded:: 2.10

    Iterate rests forward in `expr`::

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

        >>> for rest in iterationtools.iterate_rests_in_expr(staff):
        ...   rest
        Rest('r8')
        Rest('r2')

    Iterate rests backward in `expr`::

        >>> for rest in iterationtools.iterate_rests_in_expr(staff, reverse=True):
        ...   rest
        Rest('r2')
        Rest('r8')

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import iterationtools

    return iterationtools.iterate_components_in_expr(
        expr, klass=resttools.Rest, reverse=reverse, start=start, stop=stop)
