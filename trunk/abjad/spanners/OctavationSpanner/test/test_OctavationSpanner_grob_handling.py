from abjad import *


def test_OctavationSpanner_grob_handling_01( ):
   '''
   The Abjad Octavation spanner handles the LilyPond OttavaBracket grob.
   Note the need to promot OttavaBracket grob overrides to the
   LilyPond Staff context.
   '''

   t = Voice(macros.scale(4))
   p = OctavationSpanner(t[ : ], 1)
   p.override.staff.ottava_bracket.staff_position = 4

   r'''
   \new Voice {
      \override Staff.OttavaBracket #'staff-position = #4
      \ottava #1
      c'8
      d'8
      e'8
      f'8
      \ottava #0
      \revert Staff.OttavaBracket #'staff-position
   }
   '''

   assert t.format == "\\new Voice {\n\t\\override Staff.OttavaBracket #'staff-position = #4\n\t\\ottava #1\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\ottava #0\n\t\\revert Staff.OttavaBracket #'staff-position\n}"
