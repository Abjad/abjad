from abjad import *


def test_container_slip_01( ):
   '''Containers can 'slip out' of score structure.'''

   t = Staff(Sequential(run(2)) * 2)
   diatonicize(t)
   p = Beam(t.leaves)

   r'''\new Staff {
           {
                   c'8 [
                   d'8
           }
           {
                   e'8
                   f'8 ]
           }
   }'''

   sequential = t[0]
   t[0].slip( )

   r'''\new Staff {
           c'8 [
           d'8
           {
                   e'8
                   f'8 ]
           }
   }'''
   
   assert check(t)
   assert len(sequential) == 0
   assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
