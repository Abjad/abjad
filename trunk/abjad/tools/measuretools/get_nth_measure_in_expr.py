from abjad.tools import componenttools


# TODO: implement iterationtools.iterate_measures_in_expr(expr, i=0, j=None).
def get_nth_measure_in_expr(expr, n=0):
    r'''.. versionadded:: 2.0

    Get nth measure in `expr`::

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

    Read forward for positive values of `n`. ::

        >>> for n in range(3):
        ...     measuretools.get_nth_measure_in_expr(staff, n)
        ...
        Measure(2/8, [c'8, d'8])
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [g'8, a'8])

    Read backward for negative values of `n`. ::

        >>> for n in range(3, -1, -1):
        ...     measuretools.get_nth_measure_in_expr(staff, n)
        ...
        Measure(2/8, [g'8, a'8])
        Measure(2/8, [e'8, f'8])
        Measure(2/8, [c'8, d'8])

    .. versionchanged:: 2.0
        renamed ``iterate.get_nth_measure()`` to
        ``measuretools.get_nth_measure_in_expr()``.
    '''
    from abjad.tools import measuretools

    return componenttools.get_nth_component_in_expr(expr, measuretools.Measure, n)
