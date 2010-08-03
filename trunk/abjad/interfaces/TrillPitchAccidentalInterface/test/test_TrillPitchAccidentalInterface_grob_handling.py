from abjad import *


def test_TrillPitchAccidentalInterface_grob_handling_01( ):

   t = Staff(macros.scale(4))
   t.trill_pitch_accidental.staff_padding = 2
   t.trill_pitch_accidental.Y_extent = (-1.5, 1.5)

   r'''
   \new Staff \with {
           \override TrillPitchAccidental #'Y-extent = #'(-1.5 . 1.5)
           \override TrillPitchAccidental #'staff-padding = #2
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override TrillPitchAccidental #'Y-extent = #'(-1.5 . 1.5)\n\t\\override TrillPitchAccidental #'staff-padding = #2\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
