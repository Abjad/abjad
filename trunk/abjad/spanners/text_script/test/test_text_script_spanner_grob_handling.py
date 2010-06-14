from abjad import *


def test_text_script_spanner_grob_handling_01( ):
   '''Abjad TextScriptSpanner handles the LilyPond TextScript grob.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   text_script_spanner = TextScriptSpanner(t[:])
   text_script_spanner.color = 'red'

   r'''
   \new Staff {
           \override TextScript #'color = #red
           c'8
           d'8
           e'8
           f'8
           \revert TextScript #'color
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\override TextScript #'color = #red\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert TextScript #'color\n}"
