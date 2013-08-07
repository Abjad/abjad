# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_measuretools_get_one_indexed_measure_number_in_expr_01():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    assert measuretools.get_one_indexed_measure_number_in_expr(staff, 1) is staff[0]
    assert measuretools.get_one_indexed_measure_number_in_expr(staff, 2) is staff[1]
    assert measuretools.get_one_indexed_measure_number_in_expr(staff, 3) is staff[2]



def test_measuretools_get_one_indexed_measure_number_in_expr_02():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    assert py.test.raises(ValueError, 'measuretools.get_one_indexed_measure_number_in_expr(staff, -1)')
