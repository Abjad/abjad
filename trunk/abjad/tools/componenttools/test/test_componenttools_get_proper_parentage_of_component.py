from abjad import *


def test_ParentageInterface_interface_proper_01( ):

   tuplet = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
   staff = Staff([tuplet])
   note = staff.leaves[0]

   r'''
   \new Staff {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
   }
   '''

   #assert len(note.parentage.proper_parentage) == 2
   #assert note.parentage.proper_parentage[0] is tuplet
   #assert note.parentage.proper_parentage[1] is staff

   proper_parentage = componenttools.get_proper_parentage_of_component(note)
   assert len(proper_parentage) == 2
   assert proper_parentage[0] is tuplet
   assert proper_parentage[1] is staff
