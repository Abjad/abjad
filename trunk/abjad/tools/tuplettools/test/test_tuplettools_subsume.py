from abjad import *


def test_tuplettools_subsume_01( ):
   
   t = Voice(FixedDurationTuplet((2, 8), construct.run(3)) * 2)
   pitchtools.diatonicize(t)

   r'''\new Voice {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }'''

   tuplettools.subsume(t[0])

   r'''\new Voice {
           \times 2/3 {
                   c'8
           }
           \times 2/3 {
                   d'8
           }
           \times 2/3 {
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8\n\t}\n\t\\times 2/3 {\n\t\td'8\n\t}\n\t\\times 2/3 {\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t}\n}"
