from abjad import *


def test_leaftools_make_first_n_notes_in_ascending_diatonic_scale_01( ):
   '''Allow nonassignable durations.'''

   t = Staff(macros.scale(2, (5, 16)))

   r'''
   \new Staff {
        c'4 ~
        c'16
        d'4 ~
        d'16
   }
   '''

   assert t.format == "\\new Staff {\n\tc'4 ~\n\tc'16\n\td'4 ~\n\td'16\n}"
