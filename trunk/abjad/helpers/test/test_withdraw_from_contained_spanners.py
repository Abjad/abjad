from abjad import *
from abjad.helpers.withdraw_from_contained_spanners import \
   _withdraw_from_contained_spanners


def test_withdraw_from_contained_spanners_01( ):
   '''Unspan every component in components.
      Navigate down into components and traverse deeply.'''

   t = Staff(scale(4))
   Beam(t)
   Crescendo(t[:])

   _withdraw_from_contained_spanners([t])

   r'''\new Staff {
      c'8
      d'8
      e'8
      f'8
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_withdraw_from_contained_spanners_02( ):
   '''Docs.'''

   t = Staff(Container(run(2)) * 3)
   diatonicize(t)
   Beam(t.leaves[:3])
   Beam(t.leaves[3:])

   r'''\new Staff {
      {
         c'8 [
         d'8
      }
      {
         e'8 ]
         f'8 [
      }
      {
         g'8
         a'8 ]
      }
   }'''

   _withdraw_from_contained_spanners([t[1]])

   r'''\new Staff {
      {
         c'8 [
         d'8 ]
      }
      {
         e'8
         f'8
      }
      {
         g'8 [
         a'8 ]
      }
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
