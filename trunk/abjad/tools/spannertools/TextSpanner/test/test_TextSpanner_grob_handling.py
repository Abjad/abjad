from abjad import *


def test_TextSpanner_grob_handling_01( ):
   '''Abjad TextSpanner handles LilyPond TextSpanner grob.'''

   t = Staff(notetools.make_repeated_notes(4))
   p = spannertools.TextSpanner(t[:])
   p.override.text_spanner.font_shape = 'italic'

   r'''
   \new Staff {
           \override TextSpanner #'font-shape = #'italic
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
           \revert TextSpanner #'font-shape
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\override TextSpanner #'font-shape = #'italic\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n\t\\revert TextSpanner #'font-shape\n}"
