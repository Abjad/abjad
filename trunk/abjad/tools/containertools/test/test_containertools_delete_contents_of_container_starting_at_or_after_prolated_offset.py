from abjad import *


def test_containertools_delete_contents_of_container_starting_at_or_after_prolated_offset_01( ):
   
   staff = Staff(macros.scale(4))
   BeamSpanner(staff.leaves)
   containertools.delete_contents_of_container_starting_at_or_after_prolated_offset(staff, Rational(1, 8))

   r'''
   \new Staff {
        c'8 [ ]
   }
   '''

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == "\\new Staff {\n\tc'8 [ ]\n}"


def test_containertools_delete_contents_of_container_starting_at_or_after_prolated_offset_02( ):

   staff = Staff(macros.scale(4))
   BeamSpanner(staff.leaves)
   containertools.delete_contents_of_container_starting_at_or_after_prolated_offset(staff, Rational(3, 16))

   r'''
   \new Staff {
        c'8 [
        d'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == "\\new Staff {\n\tc'8 [\n\td'8 ]\n}"
