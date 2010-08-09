from abjad import *


def test_iterate_get_leaf_at_index_from_measure_number_in_expr_01( ):

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

   assert iterate.get_leaf_at_index_from_measure_number_in_expr(t, 1, 0) is t.leaves[0]
   assert iterate.get_leaf_at_index_from_measure_number_in_expr(t, 1, 1) is t.leaves[1]
   assert iterate.get_leaf_at_index_from_measure_number_in_expr(t, 2, 0) is t.leaves[2]
   assert iterate.get_leaf_at_index_from_measure_number_in_expr(t, 2, 1) is t.leaves[3]
   assert iterate.get_leaf_at_index_from_measure_number_in_expr(t, 3, 0) is t.leaves[4]
   assert iterate.get_leaf_at_index_from_measure_number_in_expr(t, 3, 1) is t.leaves[5]
