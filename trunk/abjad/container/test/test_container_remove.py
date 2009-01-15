from abjad import *


def test_container_remove_01( ):
   '''
   Containers remove( ) leaves correctly.
   Removed leaves detach from btoh parent and spanners.
   '''

   t = Staff(scale(4))
   p = Beam(t[ : ])
   note = t[0]
   t.remove(note)

   r'''
   \new Staff {
      d'8 [
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Staff {\n\td'8 [\n\te'8\n\tf'8 ]\n}"
   assert check(t)
   
   assert note.format == "c'8"
   assert check(note)


def test_container_remove_02( ):
   '''
   Containers remove( ) nested containers correctly.
   Removed containers detach from both parent and spanners.
   '''

   t = Staff(Sequential(run(2)) * 2)
   diatonicize(t)
   sequential = t[0]
   p = Beam(t[ : ])

   r'''
   \new Staff {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8 ]
      }
   }
   '''

   t.remove(sequential)

   r'''
   \new Staff {
      {
         e'8 [
         f'8 ]
      }
   }
   '''
 
   assert t.format == "\\new Staff {\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n}"
   assert check(t)

   r'''
   {
      c'8
      d'8
   }
   '''
   
   assert sequential.format == "{\n\tc'8\n\td'8\n}"
   assert check(sequential)
