from abjad import *


def test_leaf_reattach_01( ):
   '''Leaf can detach from parentage and spanners at once.
      Fully detached leaf is well formed.
      Leaf can reattach to both parentage and spanners at once.
      Fully reattached leaf is well formed.'''

   t = Staff(scale(4))
   p = Beam(t[ : ])
   note = t[1]

   r'''
   \new Staff {
           c'8 [
           d'8
           e'8
           f'8 ]
   }
   '''

   receipt = note.detach( )

   r'''
   \new Staff {
           c'8 [
           e'8
           f'8 ]
   }
   '''

   assert check(t)
   assert check(note) 

   note.reattach(receipt)

   r'''
   \new Staff {
           c'8 [
           d'8
           e'8
           f'8 ]
   }
   '''

   assert check(t)
   assert check(note)
   assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
