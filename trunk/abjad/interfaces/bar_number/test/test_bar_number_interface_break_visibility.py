from abjad import *


def test_bar_number_interface_break_visibility_01( ):

   score = Score([Staff(construct.scale(8))])
   score.bar_number.break_visibility = schemetools.SchemeFunction(
      'end-of-line-invisible')

   r'''
   \new Score \with {
           \override BarNumber #'break-visibility = #end-of-line-invisible
   } <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
                   g'8
                   a'8
                   b'8
                   c''8
           }
   >>
   '''

   assert check.wf(score)
   assert score.format == "\\new Score \\with {\n\t\\override BarNumber #'break-visibility = #end-of-line-invisible\n} <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t\tb'8\n\t\tc''8\n\t}\n>>"
