from abjad import *


def test_contents_multiply_01( ):
   '''Multiply notes in voice.'''

   t = Voice(scale(3))
   contents_multiply(t, 2)

   r'''
   \new Voice {
      c'8
      d'8
      e'8
      c'8
      d'8
      e'8
      c'8
      d'8
      e'8
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tc'8\n\td'8\n\te'8\n\tc'8\n\td'8\n\te'8\n}"
