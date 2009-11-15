from abjad import *


def test_iterate_leaves_forward_in_01( ):

   staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
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

   generator = iterate.leaves_forward_in(staff)
   leaves = list(generator)

   assert leaves[0] is staff[0][0]
   assert leaves[1] is staff[0][1]
   assert leaves[2] is staff[1][0]
   assert leaves[3] is staff[1][1]
   assert leaves[4] is staff[2][0]
   assert leaves[5] is staff[2][1]


def test_iterate_leaves_forward_in_02( ):
   '''Optional start and stop keyword parameters.'''

   staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
   pitchtools.diatonicize(staff)

   leaves = list(iterate.leaves_forward_in(staff, start = 3))
   assert leaves[0] is staff[1][1]
   assert leaves[1] is staff[2][0]
   assert leaves[2] is staff[2][1]
   assert len(leaves) == 3

   leaves = list(iterate.leaves_forward_in(staff, start = 0, stop = 3))
   assert leaves[0] is staff[0][0]
   assert leaves[1] is staff[0][1]
   assert leaves[2] is staff[1][0]
   assert len(leaves) == 3

   leaves = list(iterate.leaves_forward_in(staff, start = 2, stop = 4))
   assert leaves[0] is staff[1][0]
   assert leaves[1] is staff[1][1]
   assert len(leaves) == 2
