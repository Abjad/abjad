from abjad import *
from abjad.tools import construct


def test_diatonicize_01( ):
   '''Diatonicize notes in staff.'''

   t = Staff(run(4))
   pitches.diatonicize(t)

   r'''\new Staff {
      c'8
      d'8
      e'8
      f'8
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_diatonicize_02( ):
   '''Diatonicize tie chains in staff.'''

   t = Staff(construct.notes(0, [(5, 32)] * 4))
   pitches.diatonicize(t)

   r'''\new Staff {
      c'8 ~
      c'32
      d'8 ~
      d'32
      e'8 ~
      e'32
      f'8 ~
      f'32
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 ~\n\tc'32\n\td'8 ~\n\td'32\n\te'8 ~\n\te'32\n\tf'8 ~\n\tf'32\n}"
