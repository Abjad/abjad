from abjad import *


def test_OverrideSpanner_format_01( ):
   '''False is an acceptable value that formats as ##f.'''

   t = Staff(macros.scale(4))
   Override(t[:], 'Staff', 'BarLine', 'stencil', False)

   r'''
   \new Staff {
           \override Staff.BarLine #'stencil = ##f
           c'8
           d'8
           e'8
           f'8
           \revert Staff.BarLine #'stencil
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\override Staff.BarLine #'stencil = ##f\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Staff.BarLine #'stencil\n}"
