from abjad import *


def test_barnumber_interface_grob_handling_01( ):
   '''Handle the *LilyPond* ``BarNumber`` grob.'''

   t = Score([Staff(construct.scale(4))])
   t.barnumber.color = 'red'

   r'''\new Score \with {
           \override BarNumber #'color = #red
   } <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>'''

   assert check.wf(t)
   assert t.format == "\\new Score \\with {\n\t\\override BarNumber #'color = #red\n} <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n>>"
