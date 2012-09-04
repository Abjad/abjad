def get_leaf_at_index_in_measure_number_in_expr(expr, measure_number, leaf_index):
    r'''.. versionadded:: 2.0

    Get leaf at `leaf_index` in `measure_number` in `expr`::

        >>> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
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

    ::

        >>> leaftools.get_leaf_at_index_in_measure_number_in_expr(t, 2, 0)
        Note("e'8")

    Return leaf or none.
    '''
    from abjad.tools import leaftools
    from abjad.tools import measuretools

    # return leaf in measure
    return leaftools.get_nth_leaf_in_expr(
        measuretools.get_one_indexed_measure_number_in_expr(expr, measure_number), leaf_index)
