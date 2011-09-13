from abjad import *


def test_measuretools_iterate_measures_backward_in_expr_01():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

    r'''
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
    '''

    measures = list(measuretools.iterate_measures_backward_in_expr(staff))

    assert measures[0] is staff[2]
    assert measures[1] is staff[1]
    assert measures[2] is staff[0]


def test_measuretools_iterate_measures_backward_in_expr_02():
    '''Optional start and stop keyword paramters.'''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

    measures = list(measuretools.iterate_measures_backward_in_expr(staff, start = 1))
    assert measures[0] is staff[1]
    assert measures[1] is staff[0]
    assert len(measures) == 2

    measures = list(measuretools.iterate_measures_backward_in_expr(staff, stop = 2))
    assert measures[0] is staff[2]
    assert measures[1] is staff[1]
    assert len(measures) == 2
