from abjad import *


def test_marktools_get_effective_dynamic_01( ):

   staff = Staff(macros.scale(4))
   marktools.DynamicMark('f')(staff, staff[2])

   r'''
   \new Staff {
      c'8
      d'8
      e'8 \f
      f'8
   }
   '''

   assert marktools.get_effective_dynamic(staff) is None
   assert marktools.get_effective_dynamic(staff[0]) is None
   assert marktools.get_effective_dynamic(staff[1]) is None
   assert marktools.get_effective_dynamic(staff[2]) == marktools.DynamicMark('f')
   assert marktools.get_effective_dynamic(staff[3]) == marktools.DynamicMark('f')
