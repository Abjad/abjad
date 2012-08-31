def iterate_components_backward_in_expr(expr, klass=None, start=0, stop=None):
    r'''.. versionadded:: 1.1

    .. note:: Deprecated. Use ``componenttools.iterate_components_in_expr()`` instead.

    Iterate components backward in `expr`::

        >>> staff = Staff(r"\times 2/3 { c'8 d'8 e'8 } \times 2/3 { f'8 g'8 a'8 }")

    ::

        >>> f(staff)
        \new Staff {
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

    ::

        >>> for x in componenttools.iterate_components_backward_in_expr(staff, Note):
        ...     x
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")
        Note("e'8")
        Note("d'8")
        Note("c'8")

    .. versionadded:: 2.0
        optional `start` and `stop` keyword parameters.

    ::

        >>> for x in componenttools.iterate_components_backward_in_expr(staff, Note, 
        ...     start=0, stop=4):
        ...     x
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")
        Note("e'8")

    ::

        >>> for x in componenttools.iterate_components_backward_in_expr(staff, Note, 
        ...     start=4):
        ...     x
        ...
        Note("d'8")
        Note("c'8")

    ::

        >>> for x in componenttools.iterate_components_backward_in_expr(staff, Note, 
        ...     start=4, stop=6):
        ...     x
        ...
        Note("d'8")
        Note("c'8")

    This function is thread-agnostic.

    .. versionchanged:: 2.0
        renamed ``iterate.backwards()`` to
        ``componenttools.iterate_components_backward_in_expr()``.
    '''
    from abjad.tools import componenttools

    return componenttools.iterate_components_in_expr(
        expr, klass=klass, reverse=True, start=start, stop=stop)
