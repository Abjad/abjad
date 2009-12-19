from abjad import *


def test_fdtuplet_fraction_01( ):
   '''Fraction format nonbinary tuplets.'''

   t = FixedDurationTuplet((3, 8), construct.scale(4))
   
   r'''
   \fraction \times 3/4 {
           c'8
           d'8
           e'8
           f'8
   }
   '''
   
   assert check.wf(t)
   assert t.format == "\\fraction \\times 3/4 {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_fdtuplet_fraction_02( ):
   '''Fraction format all augmentations, even binary ones.'''

   t = FixedDurationTuplet((4, 8), construct.scale(3))


   r'''
   \fraction \times 4/3 {
           c'8
           d'8
           e'8
   }
   '''
   
   assert check.wf(t)
   assert t.format == "\\fraction \\times 4/3 {\n\tc'8\n\td'8\n\te'8\n}"


def test_fdtuplet_fraction_03( ):
   '''Do not fraction format trivial tuplets.'''

   t = FixedDurationTuplet((3, 8), construct.scale(3))

   r'''
   {
           c'8
           d'8
           e'8
   }
   '''

   assert check.wf(t)
   print t.format
   assert t.format == "{\n\tc'8\n\td'8\n\te'8\n}"
