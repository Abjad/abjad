from abjad import *
from abjad.tools.spannertools.withdraw_from_contained import \
   _withdraw_from_contained


def test_spannertools_withdraw_from_contained_01( ):
   '''Unspan every component in components.
      Navigate down into components and traverse deeply.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(t)
   Crescendo(t[:])

   _withdraw_from_contained([t])

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_spannertools_withdraw_from_contained_02( ):
   '''Docs.'''

   t = Staff(Container(leaftools.make_repeated_notes(2)) * 3)
   pitchtools.diatonicize(t)
   Beam(t.leaves[:3])
   Beam(t.leaves[3:])

   r'''
   \new Staff {
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
   }
   '''

   _withdraw_from_contained([t[1]])

   r'''
   \new Staff {
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
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
