def iterate_leaves_backward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    .. note:: Deprecated. Use ``leaftools.iterate_leafs_in_expr()`` instead.

    Iterate leaves backward in `expr`::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
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

        >>> for leaf in leaftools.iterate_leaves_backward_in_expr(staff):
        ...     leaf
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")
        Note("e'8")
        Note("d'8")
        Note("c'8")

    Use the optional `start` and `stop` keyword parameters to control
    the indices of iteration. ::

        >>> for leaf in leaftools.iterate_leaves_backward_in_expr(staff, start=3):
        ...     leaf
        ...
        Note("e'8")
        Note("d'8")
        Note("c'8")

    ::

        >>> for leaf in leaftools.iterate_leaves_backward_in_expr(staff, start=0, stop=3):
        ...     leaf
        ...
        Note("a'8")
        Note("g'8")
        Note("f'8")

    ::

        >>> for leaf in leaftools.iterate_leaves_backward_in_expr(staff, start=2, stop=4):
        ...     leaf
        ...
        Note("f'8")
        Note("e'8")

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import leaftools

    return leaftools.iterate_leaves_in_expr(expr, reverse=True, start=start, stop=stop)
