from abjad import *


def test_container_pop_01( ):
   '''
   Containers pop( ) leaves correctly.
   Popped leaves detach from both parent and spanners.
   '''

   t = Staff(scale(4))
   p = Beam(t[ : ])
   note = t.pop(-1)

   r'''
   \new Staff {
      c'8 [
      d'8
      e'8 ]
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\te'8 ]\n}"
   assert note.format == "f'8" 
   assert not note.spanners.spanned
   assert check(t)
   assert check(note)


def test_container_pop_02( ):
   '''
   Containers pop( ) nested containers correctly.
   Popped containers detach from both parent and spanners.
   '''

   t = Staff(Sequential(run(2)) * 2)
   diatonicize(t)
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

   sequential = t.pop( )

   r'''
   \new Staff {
      {
         c'8 [
         d'8 ]
      }
   }
   '''

   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n}"
   assert check(t)

   r'''
   {
      e'8
      f'8
   }
   '''

   assert sequential.format == "{\n\te'8\n\tf'8\n}"
   assert check(sequential)
