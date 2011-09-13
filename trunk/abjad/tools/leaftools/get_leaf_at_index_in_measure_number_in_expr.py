from abjad.tools.leaftools.get_nth_leaf_in_expr import get_nth_leaf_in_expr


def get_leaf_at_index_in_measure_number_in_expr(expr, measure_number, leaf_index):
    r'''.. versionadded:: 2.0

    Get leaf at `leaf_index` in `measure_number` in `expr`::

        abjad> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
        abjad> f(t)
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 2/8
                e'8
                f'8
            }
            {
                \time 2/8
                g'8
                a'8
            }
        }

    ::

        abjad> leaftools.get_leaf_at_index_in_measure_number_in_expr(t, 2, 0)
        Note("e'8")

    Return leaf or none.
    '''
    from abjad.tools.measuretools.get_one_indexed_measure_number_in_expr import get_one_indexed_measure_number_in_expr

    # return leaf in measure
    return get_nth_leaf_in_expr(
        get_one_indexed_measure_number_in_expr(expr, measure_number), leaf_index)
