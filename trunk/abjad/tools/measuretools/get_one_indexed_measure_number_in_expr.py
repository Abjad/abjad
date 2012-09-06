def get_one_indexed_measure_number_in_expr(expr, measure_number):
    r'''.. versionadded:: 2.0

    Get one-indexed `measure_number` in `expr`::

        >>> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    ::

        >>> f(t)
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
        >>> measuretools.get_one_indexed_measure_number_in_expr(t, 3)
        Measure(2/8, [g'8, a'8])

    Note that measures number from ``1``.
    '''
    from abjad.tools import measuretools

    # check input
    if measure_number < 1:
        raise ValueError('measure numbers allow only positive integers.')

    # calculate measure index
    measure_index = measure_number - 1

    # return measure
    return measuretools.get_nth_measure_in_expr(expr, measure_index)
