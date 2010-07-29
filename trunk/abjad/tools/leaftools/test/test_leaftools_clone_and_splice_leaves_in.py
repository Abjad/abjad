from abjad import *


def test_leaftools_clone_and_splice_leaves_in_01( ):
   '''Multiply each leaf in voice by 1.'''

   t = Voice(macros.scale(3))
   p = Beam(t[:])
   leaftools.clone_and_splice_leaves_in(t, total = 2)

   r'''
   \new Voice {
      c'8 [
      c'8
      d'8
      d'8
      e'8
      e'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\tc'8\n\td'8\n\td'8\n\te'8\n\te'8 ]\n}"


def test_leaftools_clone_and_splice_leaves_in_02( ):
   '''Multiply each leaf in voice by 2.'''

   t = Voice(macros.scale(3))
   Beam(t[:])
   leaftools.clone_and_splice_leaves_in(t, total = 3)

   r'''
   \new Voice {
      c'8 [
      c'8
      c'8
      d'8
      d'8
      d'8
      e'8
      e'8
      e'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\tc'8\n\tc'8\n\td'8\n\td'8\n\td'8\n\te'8\n\te'8\n\te'8 ]\n}"
