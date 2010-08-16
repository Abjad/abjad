from abjad import *


def test_MultiMeasureRestInterface_grob_handling_01( ):
   '''Override LilyPond MultiMeasureRestGrob.'''

   staff = Staff([Note(0, (1, 4))])
   staff.override.multi_measure_rest.expand_limit = 12

   r'''
   \new Staff \with {
      \override MultiMeasureRest #'expand-limit = #12
   } {
      c'4
   }
   '''

   assert staff.format == "\\new Staff \\with {\n\t\\override MultiMeasureRest #'expand-limit = #12\n} {\n\tc'4\n}"
