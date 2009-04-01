from abjad import *


def test_spanner_pop_01( ):
   '''Remove and return rightmost component in spanner.'''

   t = Voice(Container(run(2)) * 3)
   diatonicize(t)
   p = Beam(t[:])
   
   r'''\new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }'''

   result = p.pop( )

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

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8\n\t\ta'8\n\t}\n}"
   assert result is t[-1]
