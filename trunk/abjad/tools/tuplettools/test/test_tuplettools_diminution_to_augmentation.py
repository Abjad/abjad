from abjad import *


def test_tuplettools_diminution_to_augmentation_01( ):

   tuplet = FixedDurationTuplet((2, 8), construct.scale(3))

   r'''
   \times 2/3 {
           c'8
           d'8
           e'8
   }
   '''

   tuplettools.diminution_to_augmentation(tuplet)

   r'''
   \times 4/3 {
           c'16
           d'16
           e'16
   }
   '''

   assert check.wf(tuplet)
   assert tuplet.format == "\\times 4/3 {\n\tc'16\n\td'16\n\te'16\n}"
