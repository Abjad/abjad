from abjad import *


def test_componenttools_component_to_tuplet_depth_01( ):

   tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
   staff = Staff([tuplet])
   
   assert componenttools.component_to_tuplet_depth(staff) == 0
   assert componenttools.component_to_tuplet_depth(tuplet) == 0
   assert componenttools.component_to_tuplet_depth(staff.leaves[0]) == 1
   assert componenttools.component_to_tuplet_depth(staff.leaves[1]) == 1
   assert componenttools.component_to_tuplet_depth(staff.leaves[2]) == 1
