from abjad import *


def test_parentage_interface_proper_01( ):

   tuplet = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
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

   assert len(note.parentage.proper) == 2
   assert note.parentage.proper[0] is tuplet
   assert note.parentage.proper[1] is staff
