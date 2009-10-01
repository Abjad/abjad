from abjad import *


def test_nonmusicalpapercolumn_interface_grob_handling_01( ):
   '''Abjad NonMusicalPaperColumnInterface handles the LilyPond
   NonMusicalPaperColumn grob.'''

   t = Score([Staff(construct.scale(4))])
   t.nonmusicalpapercolumn.line_break_permission = False
   t.nonmusicalpapercolumn.page_break_permission = False

   r'''
   \new Score \with {
           \override NonMusicalPaperColumn #'line-break-permission = ##f
           \override NonMusicalPaperColumn #'page-break-permission = ##f
   } <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>
   '''

   assert check.wf(t)
   assert t.format == "\\new Score \\with {\n\t\\override NonMusicalPaperColumn #'line-break-permission = ##f\n\t\\override NonMusicalPaperColumn #'page-break-permission = ##f\n} <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n>>"
