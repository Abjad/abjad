from abjad import *


def test_measuretools_get_nth_measure_in_expr_01():

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

    assert measuretools.get_nth_measure_in_expr(staff, 0) is staff[0]
    assert measuretools.get_nth_measure_in_expr(staff, 1) is staff[1]
    assert measuretools.get_nth_measure_in_expr(staff, 2) is staff[2]


def test_measuretools_get_nth_measure_in_expr_02():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

    assert measuretools.get_nth_measure_in_expr(staff, -1) is staff[2]
    assert measuretools.get_nth_measure_in_expr(staff, -2) is staff[1]
    assert measuretools.get_nth_measure_in_expr(staff, -3) is staff[0]
