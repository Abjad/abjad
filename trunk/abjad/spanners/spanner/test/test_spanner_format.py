from abjad import *


def test_spanner_format_01( ):
   '''Base Spanner class makes no format-time contributions.
   However, base spanner causes no explosions at format-time, either.
   '''

   t = Staff(construct.scale(4))
   p = Spanner(t[:])

   r'''
   \new Staff {
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
