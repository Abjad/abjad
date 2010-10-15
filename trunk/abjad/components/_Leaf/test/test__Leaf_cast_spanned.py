from abjad import *


def test__Leaf_cast_spanned_01( ):
   '''
   Spanned leaves cast correctly.
   '''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   rest = Rest(t[-1])
   componenttools.move_parentage_and_spanners_from_components_to_components(t[-1:], [rest])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      r8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tr8 ]\n}"


def test__Leaf_cast_spanned_02( ):
   '''
   Spanned leaves cast correctly.
   '''

   t = Voice(macros.scale(4))
   spannertools.BeamSpanner(t[:])
   for note in t:
      rest = Rest(note)
      componenttools.move_parentage_and_spanners_from_components_to_components([note], [rest])

   r'''
   \new Voice {
      r8 [
      r8
      r8
      r8 ]
   }
   '''

   assert t.format == '\\new Voice {\n\tr8 [\n\tr8\n\tr8\n\tr8 ]\n}'
