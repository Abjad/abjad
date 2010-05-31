from abjad import *


def test_containertools_remove_empty_01( ):

   staff = Staff(Container(construct.run(2)) * 4)
   pitchtools.diatonicize(staff.leaves)
   Beam(staff[:])
   containertools.contents_delete(staff[1])
   containertools.contents_delete(staff[-1])

   r'''
   \new Staff {
        {
                c'8 [
                d'8
        }
        {
        }
        {
                g'8
                a'8 ]
        }
        {
        }
   }
   '''

   containertools.remove_empty(staff)

   r'''
   \new Staff {
        {
                c'8 [
                d'8
        }
        {
                g'8
                a'8 ]
        }
   }
   '''   

   assert check.wf(staff)
   assert staff.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
