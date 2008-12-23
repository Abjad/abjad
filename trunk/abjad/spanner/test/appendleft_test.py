from abjad import *


def test_appendleft_01( ):
   '''
   Spanner appends one container to the left.
   '''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p  = Beam(t[1])

   r'''
   \new Voice {
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
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"

   assert len(p.components) == 1

   p.appendleft(t[0])

   r'''
   \new Voice {
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
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"

   assert len(p.components) == 2
 

def test_appendleft_02( ):
   '''
   Spanner appends one leaf to the left.
   '''
   
   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
   p  = Beam(t[1])

   r'''
   \new Voice {
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
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"

   assert len(p.components) == 1

   p.appendleft(t[0][1])

   r'''
   \new Voice {
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
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8 [\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"

   assert len(p.components) == 2
