from abjad import *


def test_cut_by_duration_01( ):
   '''Trim the first 'duration' of time from 'component'.
      When 'component' is a leaf, shorten duration of leaf.
      When 'component' is a container, remove contents from container.
      Add ties or duration-modification tuplets as necessary.'''

   t = Voice(scale(4))
   Beam(t[:])

   cut.by_duration(t, Rational(1, 8) + Rational(1, 20))

   r'''\new Voice {
           \times 4/5 {
                   d'16. [
           }
           e'8
           f'8 ]
   }'''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\\times 4/5 {\n\t\td'16. [\n\t}\n\te'8\n\tf'8 ]\n}"


def test_cut_by_duration_02( ):

   t = Voice(scale(4))
   Beam(t[:])

   cut.by_duration(t, Rational(3, 16))

   r'''\new Voice {
           d'16 [
           e'8
           f'8 ]
   }'''
   
   assert check(t)
   assert t.format == "\\new Voice {\n\td'16 [\n\te'8\n\tf'8 ]\n}"
