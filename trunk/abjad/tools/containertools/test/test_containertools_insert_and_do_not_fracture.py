from abjad import *


def test_containertools_insert_and_do_not_fracture_01( ):

   staff = Staff(construct.scale(4))
   Beam(staff.leaves)
   containertools.insert_and_do_not_fracture(staff, 1, Note("cs'8"))

   r'''
   \new Staff {
        c'8 [
        cs'8
        d'8
        e'8
        f'8 ]
   }
   '''

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\te'8\n\tf'8 ]\n}"
