from abjad import *


def test_leaf_detach_01( ):
   '''
   Unspanned leaves detach from parent containers.
   '''

   t = Staff(scale(4))
   note = t[1]
   note.detach( )

   r'''
   \new Staff {
           c'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8\n\te'8\n\tf'8\n}"
   
   assert check(t)
   assert check(note)
   assert note._parent is None


def test_leaf_detach_02( ):
   '''
   Spanned leaves detach from parent containers.
   Spanners continue to attach to detached leaves.
   '''

   t = Staff([Voice(scale(4))])
   p = Beam(t.leaves)

   r'''
   \new Staff {
           \new Voice {
                   c'8 [
                   d'8
                   e'8
                   f'8 ]
           }
   }
   '''

   note = t.leaves[0]
   t.embed(0, note.detach( ))

   r'''
   \new Staff {
           c'8 [
           \new Voice {
                   d'8
                   e'8
                   f'8 ]
           }
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\t\\new Voice {\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"

   assert check(t)
   assert check(note)
