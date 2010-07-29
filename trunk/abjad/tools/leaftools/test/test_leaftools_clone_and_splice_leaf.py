from abjad import *


def test_leaftools_clone_and_splice_leaf_01( ):

   staff = Staff(macros.scale(4))
   Beam(staff.leaves)

   r'''
   \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
   }
   '''

   leaftools.clone_and_splice_leaf(staff[0], total = 3)

   r'''
   \new Staff {
        c'8 [
        c'8
        c'8
        d'8
        e'8
        f'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == "\\new Staff {\n\tc'8 [\n\tc'8\n\tc'8\n\td'8\n\te'8\n\tf'8 ]\n}"   
