from abjad import *


def test_SystemStartBarInterface_grob_handling_01( ):


   score = Score([StaffGroup([Staff(notetools.make_repeated_notes(8))])])
   score.system_start_bar.collapse_height = 0
   score.system_start_bar.color = 'red'

   r'''
   \new Score \with {
           \override SystemStartBar #'collapse-height = #0
           \override SystemStartBar #'color = #red
   } <<
           \new StaffGroup <<
                   \new Staff {
                           c'8
                           c'8
                           c'8
                           c'8
                           c'8
                           c'8
                           c'8
                           c'8
                   }
           >>
   >>
   '''

   assert score.format == "\\new Score \\with {\n\t\\override SystemStartBar #'collapse-height = #0\n\t\\override SystemStartBar #'color = #red\n} <<\n\t\\new StaffGroup <<\n\t\t\\new Staff {\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8\n\t\t}\n\t>>\n>>"
