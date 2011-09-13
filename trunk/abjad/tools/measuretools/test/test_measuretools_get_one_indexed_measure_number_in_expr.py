from abjad import *
import py.test


def test_measuretools_get_one_indexed_measure_number_in_expr_01():

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    assert measuretools.get_one_indexed_measure_number_in_expr(t, 1) is t[0]
    assert measuretools.get_one_indexed_measure_number_in_expr(t, 2) is t[1]
    assert measuretools.get_one_indexed_measure_number_in_expr(t, 3) is t[2]



def test_measuretools_get_one_indexed_measure_number_in_expr_02():

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    assert py.test.raises(ValueError, 'measuretools.get_one_indexed_measure_number_in_expr(t, -1)')
