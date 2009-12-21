from abjad import *


def test_leaftools_subruns_of_type_01( ):

   staff = Staff(construct.leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
   t = list(leaftools.subruns_of_type(staff, Note))

   assert t == [(staff[0], staff[1], staff[2]), (staff[5], staff[6])]
