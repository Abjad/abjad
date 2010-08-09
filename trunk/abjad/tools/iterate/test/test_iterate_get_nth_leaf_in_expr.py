from abjad import *


def test_iterate_get_nth_leaf_in_expr_01( ):
   '''Read forwards for positive n.'''

   staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

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

   assert iterate.get_nth_leaf_in_expr(staff, 0) is staff[0][0]
   assert iterate.get_nth_leaf_in_expr(staff, 1) is staff[0][1]
   assert iterate.get_nth_leaf_in_expr(staff, 2) is staff[1][0]
   assert iterate.get_nth_leaf_in_expr(staff, 3) is staff[1][1]
   assert iterate.get_nth_leaf_in_expr(staff, 4) is staff[2][0]
   assert iterate.get_nth_leaf_in_expr(staff, 5) is staff[2][1]


def test_iterate_get_nth_leaf_in_expr_02( ):
   '''Read backwards for negative n.'''

   staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

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

   assert iterate.get_nth_leaf_in_expr(staff, -1) is staff[2][1]
   assert iterate.get_nth_leaf_in_expr(staff, -2) is staff[2][0]
   assert iterate.get_nth_leaf_in_expr(staff, -3) is staff[1][1]
   assert iterate.get_nth_leaf_in_expr(staff, -4) is staff[1][0]
   assert iterate.get_nth_leaf_in_expr(staff, -5) is staff[0][1]
   assert iterate.get_nth_leaf_in_expr(staff, -6) is staff[0][0]
