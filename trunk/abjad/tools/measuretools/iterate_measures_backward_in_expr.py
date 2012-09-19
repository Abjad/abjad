def iterate_measures_backward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    .. note:: Deprecated. Use ``measuretools.iterate_measures_in_expr()`` instead.

    Iterate measures backward in `expr`::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    ::

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

        >>> for measure in measuretools.iterate_measures_backward_in_expr(staff):
        ...     measure
        ...
        Measure(2/8, [g'8, a'8])
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [c'8, d'8])

    Use the optional `start` and `stop` keyword parameters
    to control indices of iteration. ::

        >>> for measure in measuretools.iterate_measures_backward_in_expr(staff, start=1):
        ...     measure
        ...
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [c'8, d'8])

    ::

        >>> for measure in measuretools.iterate_measures_backward_in_expr(staff, start=0, stop=2):
        ...     measure
        ...
        Measure(2/8, [g'8, a'8])
        Measure(2/8, [e'8, f'8])

    .. versionchanged:: 2.0
        renamed ``iterate.measures_backward_in()`` to
        ``measuretools.iterate_measures_backward_in_expr()``.
    '''
    from abjad.tools import measuretools

    return measuretools.iterate_measures_in_expr(
        expr, reverse=True, start=start, stop=stop)
