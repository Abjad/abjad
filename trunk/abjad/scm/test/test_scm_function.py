from abjad import *


def test_scm_function_01( ):
   '''Scheme functions known to LilyPond format with no apostrophe.'''
   t = Staff(scale(4))
   t.meter.break_visibility = Function('end-of-line-invisible')

   r'''
   \new Staff \with {
      \override TimeSignature #'break-visibility = #end-of-line-invisible
   } {
      c'8
      d'8
      e'8
      f'8
   }
   '''

   assert t.format == "\\new Staff \\with {\n\t\\override TimeSignature #'break-visibility = #end-of-line-invisible\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
