from abjad import *


def test_containertools_contents_delete_starting_not_before_prolated_offset_01( ):
   
   staff = Staff(construct.scale(4))
   Beam(staff.leaves)
   containertools.contents_delete_starting_not_before_prolated_offset(staff, Rational(1, 8))

   r'''
   \new Staff {
        c'8 [ ]
   }
   '''

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\tc'8 [ ]\n}"


def test_containertools_contents_delete_starting_not_before_prolated_offset_02( ):

   staff = Staff(construct.scale(4))
   Beam(staff.leaves)
   containertools.contents_delete_starting_not_before_prolated_offset(staff, Rational(3, 16))

   r'''
   \new Staff {
        c'8 [
        d'8 ]
   }
   '''

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\tc'8 [\n\td'8 ]\n}"
