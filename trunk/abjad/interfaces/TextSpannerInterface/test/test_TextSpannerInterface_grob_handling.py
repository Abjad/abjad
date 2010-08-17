from abjad import *


def test_TextSpannerInterface_grob_handling_01( ):
   '''Abjad TextSpannerInterface handles LilyPond TextSpanner grob.'''

   t = Staff(macros.scale(4))
   t.override.text_spanner.staff_padding = 6
   spannertools.TextSpanner(t[:])

   r'''
   \new Staff \with {
           \override TextSpanner #'staff-padding = #6
   } {
           c'8 \startTextSpan
           d'8
           e'8
           f'8 \stopTextSpan
   }
   '''
   
   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff \\with {\n\t\\override TextSpanner #'staff-padding = #6\n} {\n\tc'8 \\startTextSpan\n\td'8\n\te'8\n\tf'8 \\stopTextSpan\n}"
