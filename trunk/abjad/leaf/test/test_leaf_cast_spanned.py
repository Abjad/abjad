from abjad import *


def test_leaf_cast_spanned_01( ):
   '''
   Spanned leaves cast correctly.
   '''

   t = Voice(scale(4))
   Beam(t[ : ])
   Rest(t[-1])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      r8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tr8 ]\n}"


def test_leaf_cast_spanned_02( ):
   '''
   Spanned leaves cast correctly.
   '''

   t = Voice(scale(4))
   Beam(t[ : ])
   for note in t:
      Rest(note)

   r'''
   \new Voice {
      r8 [
      r8
      r8
      r8 ]
   }
   '''

   assert t.format == '\\new Voice {\n\tr8 [\n\tr8\n\tr8\n\tr8 ]\n}'
