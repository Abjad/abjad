from abjad import *


def test_pop_01( ):
   '''Components can be poped. Poped components are fractured correctly.'''
   t = Staff(Voice(Note(0, (1,8)) * 8)* 2)
   #Beam(t)
   Beam(t[ : ])
   v = t[1]
   assert t.format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t\\new Voice {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}" 
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
   assert v.format == "\\new Voice {\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ]\n}"

   '''
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
   '''
   x = t.pop( )
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
   assert v.format == "\\new Voice {\n\tc'8 [\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8 ]\n}"
   '''
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
   '''
   assert x.format == v.format
   assert x == v
   assert id(x) == id(v)

