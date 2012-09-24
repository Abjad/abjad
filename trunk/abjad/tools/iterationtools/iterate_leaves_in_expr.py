from abjad.tools import leaftools


def iterate_leaves_in_expr(expr, reverse=False, start=0, stop=None):
    r'''.. versionadded:: 2.10

    Iterate leaves forward in `expr`::

        >>> staff = Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
            }
        }

    ::

        >>> for leaf in iterationtools.iterate_leaves_in_expr(staff):
        ...     leaf
        ...
        Note("c'8")
        Note("d'8")
        Note("e'8")
        Note("f'8")
        Note("g'8")
        Note("a'8")

    Use the optional `start` and `stop` keyword parameters to control
    the start and stop indices of iteration. ::

        >>> for leaf in iterationtools.iterate_leaves_in_expr(staff, start=3):
        ...     leaf
        ...
        Note("f'8")
        Note("g'8")
        Note("a'8")

    ::

        >>> for leaf in iterationtools.iterate_leaves_in_expr(staff, start=0, stop=3):
        ...     leaf
        ...
        Note("c'8")
        Note("d'8")
        Note("e'8")

    ::

        >>> for leaf in iterationtools.iterate_leaves_in_expr(staff, start=2, stop=4):
        ...     leaf
        ...
        Note("e'8")
        Note("f'8")

    Iterate leaves backward in `expr`:

    ::

        >>> for leaf in iterationtools.iterate_leaves_in_expr(staff, reverse=True):
        ...     leaf
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")
        Note("e'8")
        Note("d'8")
        Note("c'8")

    ::

        >>> for leaf in iterationtools.iterate_leaves_in_expr(staff, start=3, reverse=True):
        ...     leaf
        ...
        Note("e'8")
        Note("d'8")
        Note("c'8")

    ::

        >>> for leaf in iterationtools.iterate_leaves_in_expr(staff, start=0, stop=3, reverse=True):
        ...     leaf
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")

    ::

        >>> for leaf in iterationtools.iterate_leaves_in_expr(staff, start=2, stop=4, reverse=True):
        ...     leaf
        ...
        Note("f'8")
        Note("e'8")

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import iterationtools

    return iterationtools.iterate_components_in_expr(
        expr, klass=leaftools.Leaf, reverse=reverse, start=start, stop=stop)

