from abjad import *


def test_tuplettools_augmentation_to_diminution_01( ):

   tuplet = FixedDurationTuplet((2, 4), construct.scale(3))
   
   r'''
   \times 4/3 {
           c'8
           d'8
           e'8
   }
   '''

   tuplettools.augmentation_to_diminution(tuplet)

   r'''
   \times 2/3 {
           c'4
           d'4
           e'4
   }
   '''

   assert check.wf(tuplet)
   assert tuplet.format == "\\times 2/3 {\n\tc'4\n\td'4\n\te'4\n}"

