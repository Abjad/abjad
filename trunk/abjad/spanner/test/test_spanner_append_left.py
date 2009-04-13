from abjad import *


def test_append_left_01( ):
   '''Append container to the left.'''

   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   p = Beam(t[1])

   r'''\new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }'''

   p.append_left(t[0])

   r'''\new Voice {
           {
                   c'8 [
                   d'8
           }
           {
                   e'8
                   f'8 ]
           }
           {
                   g'8
                   a'8
           }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
 

def test_append_left_02( ):
   '''Spanner appends one leaf to the right.'''
   
   t = Voice(Container(construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   p = Beam(t[1])

   r'''\new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8
         a'8
      }
   }'''

   p.append_left(t[0][-1])

   r'''\new Voice {
           {
                   c'8
                   d'8 [
           }
           {
                   e'8
                   f'8 ]
           }
           {
                   g'8
                   a'8
           }
   }'''

   check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8 [\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
