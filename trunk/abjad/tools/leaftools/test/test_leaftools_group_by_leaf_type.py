from abjad import *


def test_leaftools_group_by_leaf_type_01( ):

   staff = Staff(construct.leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
   t = list(leaftools.group_by_leaf_type(staff.leaves))

   assert t == [(staff[0], staff[1], staff[2]), (staff[3], staff[4]),
      (staff[5], staff[6])]
