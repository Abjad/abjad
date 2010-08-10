from abjad import *


def test_componenttools_group_topmost_components_in_expr_by_type_and_yield_groups_of_klass_01( ):

   staff = Staff(leaftools.make_leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
   t = list(componenttools.group_topmost_components_in_expr_by_type_and_yield_groups_of_klass(staff, Note))

   assert t == [(staff[0], staff[1], staff[2]), (staff[5], staff[6])]
