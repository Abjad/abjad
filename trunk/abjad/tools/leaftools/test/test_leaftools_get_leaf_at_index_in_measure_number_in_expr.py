# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_get_leaf_at_index_in_measure_number_in_expr_01():

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)

    assert leaftools.get_leaf_at_index_in_measure_number_in_expr(staff, 1, 0) is staff.select_leaves()[0]
    assert leaftools.get_leaf_at_index_in_measure_number_in_expr(staff, 1, 1) is staff.select_leaves()[1]
    assert leaftools.get_leaf_at_index_in_measure_number_in_expr(staff, 2, 0) is staff.select_leaves()[2]
    assert leaftools.get_leaf_at_index_in_measure_number_in_expr(staff, 2, 1) is staff.select_leaves()[3]
    assert leaftools.get_leaf_at_index_in_measure_number_in_expr(staff, 3, 0) is staff.select_leaves()[4]
    assert leaftools.get_leaf_at_index_in_measure_number_in_expr(staff, 3, 1) is staff.select_leaves()[5]
