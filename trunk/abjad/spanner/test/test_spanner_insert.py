from abjad import *
import py.test


py.test.skip('Spanner changes.')

def test_insert_01( ):
   '''Spanners can insert at index 0.'''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
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

   p.insert(0, t[0][1])

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

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8 [\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"


def test_insert_02( ):
   '''Spanners can insert after last index.
      Equivalent to append.'''

   t = Voice(Sequential(run(2)) * 3)
   diatonicize(t)
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

   p.insert(len(p.components) + 1, t[2][0])

   r'''\new Voice {
      {
         c'8
         d'8
      }
      {
         e'8 [
         f'8
      }
      {
         g'8 ]
         a'8
      }
   }'''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\te'8 [\n\t\tf'8\n\t}\n\t{\n\t\tg'8 ]\n\t\ta'8\n\t}\n}"
