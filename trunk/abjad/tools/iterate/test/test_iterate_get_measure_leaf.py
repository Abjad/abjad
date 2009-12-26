from abjad import *


def test_iterate_get_measure_leaf_01( ):

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
   pitchtools.diatonicize(t)

   assert iterate.get_measure_leaf(t, 1, 0) is t.leaves[0]
   assert iterate.get_measure_leaf(t, 1, 1) is t.leaves[1]
   assert iterate.get_measure_leaf(t, 2, 0) is t.leaves[2]
   assert iterate.get_measure_leaf(t, 2, 1) is t.leaves[3]
   assert iterate.get_measure_leaf(t, 3, 0) is t.leaves[4]
   assert iterate.get_measure_leaf(t, 3, 1) is t.leaves[5]
