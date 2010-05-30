from abjad import *


def test_containertools_contents_delete_starting_after_prolated_offset_01( ):
   
   staff = Staff(construct.scale(4))
   Beam(staff.leaves)
   containertools.contents_delete_starting_after_prolated_offset(staff, Rational(1, 8))

   r'''
   \new Staff {
        c'8 [
        d'8 ]
   }
   '''

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\tc'8 [\n\td'8 ]\n}"


def test_containertools_contents_delete_starting_after_prolated_offset_02( ):

   staff = Staff(construct.scale(4))
   Beam(staff.leaves)
   containertools.contents_delete_starting_after_prolated_offset(staff, Rational(3, 16))

   r'''
   \new Staff {
        c'8 [
        d'8 ]
   }
   '''

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\tc'8 [\n\td'8 ]\n}"


def test_containertools_contents_delete_starting_after_prolated_offset_03( ):
   '''Delete nothing when no contents start after prolated offset.'''

   staff = Staff(construct.scale(4))
   Beam(staff.leaves)
   containertools.contents_delete_starting_after_prolated_offset(staff, 99)

   r'''
   \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
   }
   '''

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_containertools_contents_delete_starting_after_prolated_offset_04( ):
   '''Delete all contents when all elements start after prolated offset.'''

   staff = Staff(construct.scale(4))
   Beam(staff.leaves)
   containertools.contents_delete_starting_after_prolated_offset(staff, -99)

   r'''
   \new Staff {
   }
   '''

   assert check.wf(staff)
   assert staff.format == '\\new Staff {\n}'
