from abjad import *


def test_Comment___init___01( ):
   '''Initialize LilyPond \slurDotted command.
   '''

   staff = Staff(macros.scale(4))
   slur = spannertools.SlurSpanner(staff.leaves)
   comment_mark = marktools.Comment('beginning of note content')(staff[0])

   r'''
   \new Staff {
      % beginning of note content
      c'8 (
      d'8
      e'8
      f'8 )
   }
   '''

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == "\\new Staff {\n\t% beginning of note content\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"
