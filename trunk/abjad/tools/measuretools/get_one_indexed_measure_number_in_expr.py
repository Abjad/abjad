from abjad.tools.measuretools.get_nth_measure_in_expr import get_nth_measure_in_expr


def get_one_indexed_measure_number_in_expr(expr, measure_number):
    r'''.. versionadded:: 2.0

    Get one-indexed `measure_number` in `expr`::

        abjad> t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    ::

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
        abjad> measuretools.get_one_indexed_measure_number_in_expr(t, 3)
        Measure(2/8, [g'8, a'8])

    Note that measures number from 1.
    '''

    if measure_number < 1:
        raise ValueError('measure numbers allow only positive integers.')

    # calculate measure index
    measure_index = measure_number - 1

    # return measure
    return get_nth_measure_in_expr(expr, measure_index)
