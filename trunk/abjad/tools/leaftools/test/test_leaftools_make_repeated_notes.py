from abjad import *


def test_leaftools_make_repeated_notes_01( ):
   '''Allow nonassignable durations.'''

   t = Voice(leaftools.make_repeated_notes(2, (5, 16)))

   r'''
   \new Voice {
           c'4 ~
           c'16
           c'4 ~
           c'16
   }
   '''

   assert t.format == "\\new Voice {\n\tc'4 ~\n\tc'16\n\tc'4 ~\n\tc'16\n}"
