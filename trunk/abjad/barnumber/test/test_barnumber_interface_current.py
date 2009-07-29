from abjad import *


def test_barnumber_interface_current_01( ):
   '''Handle LilyPond ``currentBarNumber`` context setting.'''

   t = Staff(construct.scale(4))
   t[0].barnumber.current = 12
   overridetools.promote(t[0].barnumber, 'current', 'Score')

   r'''
   \new Staff {
           \set Score.currentBarNumber = #12
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\set Score.currentBarNumber = #12\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
