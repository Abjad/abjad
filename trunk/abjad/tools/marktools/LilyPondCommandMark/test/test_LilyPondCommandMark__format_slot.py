from abjad import *


def test_LilyPondCommandMark__format_slot_01( ):

   staff = Staff(macros.scale(4))
   marktools.LilyPondCommandMark('break', format_slot = 'closing')(staff[0])

   r'''
   \new Staff {
      c'8
      \break
      d'8
      e'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == "\\new Staff {\n\tc'8\n\t\\break\n\td'8\n\te'8\n\tf'8\n}"
