from abjad import *


def test_container_detach_01( ):
   '''t.detach( ) detaches container t from both spanners and parentage.'''

   t = Staff(Container(construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   p = Beam(t[ : ])
   sequential = t[0]

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

   sequential.detach( )

   r'''\new Staff {
           {
                   e'8 [
                   f'8 ]
           }
   }'''
   
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n}"

   r'''{
           c'8
           d'8
   }'''
   
   assert check.wf(sequential)
   assert sequential.format == "{\n\tc'8\n\td'8\n}"
