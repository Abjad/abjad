from abjad import *


def test_clonewp_with_parent_01( ):
   '''Copy adjacent notes in staff.'''

   t = Staff(construct.scale(4))
   u = clonewp.with_parent(t[:2])

   r'''\new Staff {
           c'8
           d'8
   }'''

   assert check.wf(t)
   assert check.wf(u)
   assert u.format == "\\new Staff {\n\tc'8\n\td'8\n}"


def test_clonewp_with_parent_02( ):
   '''Copy adjacent notes in staff.'''

   t = Staff(construct.scale(4))
   u = clonewp.with_parent(t[-2:])

   r'''\new Staff {
           e'8
           f'8
   }'''
   
   assert check.wf(t)
   assert check.wf(u)
   assert u.format == "\\new Staff {\n\te'8\n\tf'8\n}"



def test_clonewp_with_parent_03( ):
   '''Copy notes from tuplet and preserve tuplet target duration.'''

   t = FixedDurationTuplet((4, 8), construct.scale(5))
   u = clonewp.with_parent(t[:3])

   r'''\times 4/5 {
           c'8
           d'8
           e'8
   }'''

   assert isinstance(u, FixedDurationTuplet)
   assert u.duration.target == Rational(3, 10)
   assert len(u) == 3

   assert u.format == "\\times 4/5 {\n\tc'8\n\td'8\n\te'8\n}"


def test_clonewp_with_parent_04( ):
   '''Copy adjacent, whole tuplets from staff.'''

   t = Staff(FixedDurationTuplet((2, 8), construct.run(3)) * 3)
   pitchtools.diatonicize(t)
   u = clonewp.with_parent(t[1:])

   r'''\new Staff {
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
           \times 2/3 {
                   b'8
                   c''8
                   d''8
           }
   }'''

   assert check.wf(t)
   assert check.wf(u) 
   assert u.format == "\\new Staff {\n\t\\times 2/3 {\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t}\n\t\\times 2/3 {\n\t\tb'8\n\t\tc''8\n\t\td''8\n\t}\n}"
