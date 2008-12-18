from abjad import *


def test_remove_01( ):
   '''
   Components can be removed. Spanners are fractured appropriately.
   '''

   t = Staff(Voice(Note(0, (1,8)) * 8)* 2)
   #Beam(t)
   Beam(t[ : ])
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t\\new Voice {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}" 

   r'''
   \new Staff {
           \new Voice {
                   c'8 [
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
           }
           \new Voice {
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8 ]
           }
   }
   '''

   t.remove(t[0])
   assert t.format =="\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"

   '''
   \new Staff {
           \new Voice {
                   c'8 [
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8
                   c'8 ]
           }
   }
   '''
