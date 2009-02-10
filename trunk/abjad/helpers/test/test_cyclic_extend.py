from abjad import *


def test_cyclic_extend_01( ):
   '''Cyclic extend measures in voice.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 2)
   diatonicize(t)

   r'''
   \new Voice {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
   }
   '''

   cyclic_extend(t, n = 1, reps = 3)

   r'''
   \new Voice {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         e'8
         f'8
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n}"


def test_cyclic_extend_02( ):
   '''Cyclic extend tuplets in voice.'''
   
   t = Voice(FixedDurationTuplet((2, 8), run(3)) * 2)
   diatonicize(t)

   r'''
   \new Voice {
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
   }
   '''

   cyclic_extend(t, 2, 1)

   r'''
   \new Voice {
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
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t}\n\t\\times 2/3 {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t}\n}"
