from abjad import *


def test_iterate_get_nth_leaf_in_01( ):
   '''Read forwards for positive n.'''

   staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
   pitchtools.diatonicize(staff)

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

   assert iterate.get_nth_leaf_in(staff, 0) is staff[0][0]
   assert iterate.get_nth_leaf_in(staff, 1) is staff[0][1]
   assert iterate.get_nth_leaf_in(staff, 2) is staff[1][0]
   assert iterate.get_nth_leaf_in(staff, 3) is staff[1][1]
   assert iterate.get_nth_leaf_in(staff, 4) is staff[2][0]
   assert iterate.get_nth_leaf_in(staff, 5) is staff[2][1]


def test_iterate_get_nth_leaf_in_02( ):
   '''Read backwards for negative n.'''

   staff = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 3)
   pitchtools.diatonicize(staff)

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

   assert iterate.get_nth_leaf_in(staff, -1) is staff[2][1]
   assert iterate.get_nth_leaf_in(staff, -2) is staff[2][0]
   assert iterate.get_nth_leaf_in(staff, -3) is staff[1][1]
   assert iterate.get_nth_leaf_in(staff, -4) is staff[1][0]
   assert iterate.get_nth_leaf_in(staff, -5) is staff[0][1]
   assert iterate.get_nth_leaf_in(staff, -6) is staff[0][0]
