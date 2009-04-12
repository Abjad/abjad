from abjad import *


def test_leaf_detach_01( ):
   '''t.detach( ) detaches leaf t from both spanners and parentage.'''

   t = Staff(scale(4))
   p = Beam(t[ : ])
   note = t[1]
   note.detach( )

   r'''
   \new Staff {
           c'8 [
           e'8
           f'8 ]
   }
   '''
   
   assert t.format == "\\new Staff {\n\tc'8 [\n\te'8\n\tf'8 ]\n}"
   assert check.wf(t)

   assert note.format == "d'8"
   assert check.wf(note)
